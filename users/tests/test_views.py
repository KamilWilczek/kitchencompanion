import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.models import CustomUser


@pytest.mark.django_db
class TestRegisterView:
    def test_register_user(self, not_authenticated_api_client: APIClient):
        url = "/register/"
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
        url = "/register/"
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


@pytest.mark.django_db
class TestLoginView:
    def test_login_user(
        self,
        not_authenticated_api_client: APIClient,
        external_user: CustomUser,
        external_user_password: str,
    ):
        url = "/login/"
        data: dict[str, str] = {
            "email": external_user.email,
            "password": external_user_password,
        }

        response = not_authenticated_api_client.post(url, data)

        assert response.status_code == status.HTTP_200_OK, response.content
        assert "token" in response.data

        user = CustomUser.objects.get(email=external_user.email)
        assert Token.objects.filter(user=user).exists()

    def test_login_with_incorrect__nonexistent_email(
        self,
        not_authenticated_api_client: APIClient,
        external_user: CustomUser,
    ):
        url = "/login/"

        incorrect_email_data: dict[str, str] = {
            "email": "incorrect_email@example.com",
            "password": external_user.password,
        }

        response = not_authenticated_api_client.post(url, incorrect_email_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
        assert "non_field_errors" in response.data
        assert "Incorrect Credentials" in response.data["non_field_errors"]

    def test_login_with_incorrect_password(
        self,
        not_authenticated_api_client: APIClient,
        external_user: CustomUser,
    ):
        url = "/login/"

        incorrect_password_data: dict[str, str] = {
            "email": external_user.email,
            "password": "incorrectPassword",
        }

        response = not_authenticated_api_client.post(url, incorrect_password_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
        assert "non_field_errors" in response.data
        assert "Incorrect Credentials" in response.data["non_field_errors"]


@pytest.mark.django_db
class TestLogoutView:
    def test_logout_user(self, authenticated_api_client: APIClient):
        url = "/logout/"

        response = authenticated_api_client.post(url)

        assert response.status_code == status.HTTP_200_OK, response.content

        user = CustomUser.objects.get(email="testuser@example.com")
        assert not Token.objects.filter(user=user).exists()


@pytest.mark.django_db
class TestDeleteAccountView:
    def test_delete_account(
        self, authenticated_api_client: APIClient, authenticated_user: CustomUser
    ):
        url = f"/delete_account/"

        response = authenticated_api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT, response.content
        assert not CustomUser.objects.filter(pk=authenticated_user.pk).exists()

    def test_user_can_only_delete_own_account(
        self,
        authenticated_api_client: APIClient,
        authenticated_user: CustomUser,
        external_user: CustomUser,
    ):
        # Initially, both the original user and another_user should exist
        assert CustomUser.objects.filter(pk=authenticated_user.pk).exists()
        assert CustomUser.objects.filter(pk=external_user.pk).exists()

        url = f"/delete_account/"
        response = authenticated_api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT, response.content

        # After the request, only the original user's account should be deleted
        assert not CustomUser.objects.filter(pk=authenticated_user.pk).exists()
        assert CustomUser.objects.filter(pk=external_user.pk).exists()

    def test_deleted_user_cannot_access_protected_resources(
        self, authenticated_api_client: APIClient
    ):
        delete_url = "/delete_account/"
        delete_response = authenticated_api_client.delete(delete_url)
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        protected_url = "/logout/"
        protected_response = authenticated_api_client.get(protected_url)

        assert protected_response.status_code == status.HTTP_401_UNAUTHORIZED
