import pytest
from django.core import mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.models import CustomUser


@pytest.mark.django_db
class TestRegister:
    def test_register_user(self, not_authenticated_api_client: APIClient):
        url = "/auth/users/"
        data: dict[str, str] = {
            "email": "notregistereduser@example.com",
            "password": "notregistereduserpassword",
        }
        response = not_authenticated_api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED, response.content
        assert CustomUser.objects.filter(email="notregistereduser@example.com").exists()

    def test_register_with_already_registered_email(
        self, not_authenticated_api_client: APIClient, external_user: CustomUser
    ):
        url = "/auth/users/"
        data: dict[str, str] = {
            "email": external_user.email,
            "password": external_user.password,
        }

        response = not_authenticated_api_client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
        assert "email" in response.data, "Expected an error related to the email field"
        assert (
            "already" in response.data["email"][0].lower()
        ), "Expected an error message indicating the email is already in use"

    def test_registration_sends_email(self, not_authenticated_api_client: APIClient):
        url = "/auth/users/"
        data = {"email": "newuser@example.com", "password": "newpassword"}

        response = not_authenticated_api_client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED, response.content
        assert len(mail.outbox) == 1

        email = mail.outbox[0]

        assert email.subject == "Account activation on testserver"
        assert email.to == ["newuser@example.com"]
        assert "/activate/" in email.body


@pytest.mark.django_db
class TestLogin:
    def test_login_user(
        self,
        not_authenticated_api_client: APIClient,
        external_user: CustomUser,
        external_user_password: str,
    ):
        url = "/auth/token/login/"
        data: dict[str, str] = {
            "email": external_user.email,
            "password": external_user_password,
        }

        response = not_authenticated_api_client.post(url, data)

        assert response.status_code == status.HTTP_200_OK, response.content
        assert "auth_token" in response.data

        user = CustomUser.objects.get(email=external_user.email)
        assert Token.objects.filter(user=user).exists()

    def test_login_with_incorrect__nonexistent_email(
        self,
        not_authenticated_api_client: APIClient,
        external_user: CustomUser,
    ):
        url = "/auth/token/login/"

        incorrect_email_data: dict[str, str] = {
            "email": "incorrect_email@example.com",
            "password": external_user.password,
        }

        response = not_authenticated_api_client.post(url, incorrect_email_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
        assert "non_field_errors" in response.data

        assert any(
            "incorrect credentials" in error.lower()
            for error in response.data["non_field_errors"]
        )

    def test_login_with_incorrect_password(
        self,
        not_authenticated_api_client: APIClient,
        external_user: CustomUser,
    ):
        url = "/auth/token/login/"

        incorrect_password_data: dict[str, str] = {
            "email": external_user.email,
            "password": "incorrectPassword",
        }

        response = not_authenticated_api_client.post(url, incorrect_password_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
        assert "non_field_errors" in response.data
        assert any(
            "incorrect credentials" in error.lower()
            for error in response.data["non_field_errors"]
        )


@pytest.mark.django_db
class TestLogout:
    def test_logout_user(
        self, authenticated_api_client: APIClient, authenticated_user: CustomUser
    ):
        assert Token.objects.filter(user=authenticated_user).exists()

        url = "/auth/token/logout/"

        response = authenticated_api_client.post(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT, response.content

        assert not Token.objects.filter(user=authenticated_user).exists()


@pytest.mark.django_db
class TestDeleteAccount:
    def test_delete_account(
        self,
        authenticated_api_client: APIClient,
        authenticated_user: CustomUser,
        authenticated_user_password: str,
    ):
        url = "/auth/users/me/"
        data = {
            "current_password": authenticated_user_password,
        }

        response = authenticated_api_client.delete(url, data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT, response.content
        assert not CustomUser.objects.filter(pk=authenticated_user.pk).exists()

    def test_user_can_only_delete_own_account(
        self,
        authenticated_api_client: APIClient,
        authenticated_user: CustomUser,
        authenticated_user_password: str,
        external_user: CustomUser,
    ):
        # Initially, both the original user and another_user should exist
        assert CustomUser.objects.filter(pk=authenticated_user.pk).exists()
        assert CustomUser.objects.filter(pk=external_user.pk).exists()

        url = "/auth/users/me/"
        data = {
            "current_password": authenticated_user_password,
        }
        response = authenticated_api_client.delete(url, data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT, response.content

        # After the request, only the original user's account should be deleted
        assert not CustomUser.objects.filter(pk=authenticated_user.pk).exists()
        assert CustomUser.objects.filter(pk=external_user.pk).exists()

    def test_deleted_user_cannot_access_protected_resources(
        self, authenticated_api_client: APIClient, authenticated_user_password: str
    ):
        url = "/auth/users/me/"
        data = {
            "current_password": authenticated_user_password,
        }
        delete_response = authenticated_api_client.delete(url, data=data)
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        protected_url = "/auth/token/logout/"
        protected_response = authenticated_api_client.post(protected_url)

        assert protected_response.status_code == status.HTTP_401_UNAUTHORIZED
