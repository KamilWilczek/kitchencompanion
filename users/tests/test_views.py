import datetime
import json

import pytest
from axes.models import AccessAttempt, AccessLog
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import mail
from django.core.cache import cache
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from freezegun import freeze_time
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from shoppinglist.models import ShoppingList
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

    def test_register_with_long_email(self, not_authenticated_api_client: APIClient):
        long_email = "user@" + "a" * 240 + ".com"
        long_password = "P@ssw0rd" + "a" * 245

        response = not_authenticated_api_client.post(
            "/auth/users/", {"email": long_email, "password": long_password}
        )
        assert (
            response.status_code == status.HTTP_400_BAD_REQUEST
        ), "Should not allow extremely long email"

        assert "email" in response.data, "Response should contain email error"
        assert "password" in response.data, "Response should contain password error"
        assert response.data["email"] == [
            "Enter a valid email address."
        ], "Unexpected email error message"
        assert response.data["password"] == [
            "Ensure this field has no more than 128 characters."
        ], "Unexpected password error message"

    def test_register_with_special_characters(
        self, not_authenticated_api_client: APIClient
    ):
        special_email = "special.user+test@example.com"
        special_password = "P@ss!w#rd$%"

        response = not_authenticated_api_client.post(
            "/auth/users/", {"email": special_email, "password": special_password}
        )
        assert (
            response.status_code == status.HTTP_201_CREATED
        ), "Should allow special characters in email and password"

        assert "email" in response.data, "Response should contain email"
        assert response.data["email"] == special_email, "Unexpected email in response"

        user_exists = CustomUser.objects.filter(email=special_email).exists()
        assert user_exists, "User with special characters in email should be created"


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
        print("url", url)
        print("data", data)

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
        assert response.status_code == status.HTTP_403_FORBIDDEN, response.content
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
        assert response.status_code == status.HTTP_403_FORBIDDEN, response.content
        assert "non_field_errors" in response.data
        assert any(
            "incorrect credentials" in error.lower()
            for error in response.data["non_field_errors"]
        )

    def test_login_with_long_email(self, not_authenticated_api_client: APIClient):
        long_email = "user@" + "a" * 240 + ".com"
        long_password = "P@ssw0rd" + "a" * 245

        CustomUser.objects.create_user(email=long_email, password=long_password)

        response = not_authenticated_api_client.post(
            "/auth/token/login/", {"email": long_email, "password": long_password}
        )
        assert (
            response.status_code == status.HTTP_403_FORBIDDEN
        ), "Should return 403 Forbidden for validation errors"
        assert "email" in response.data, "Response should contain email error"
        assert "password" in response.data, "Response should contain password error"
        assert response.data["email"] == [
            "Enter a valid email address."
        ], "Unexpected email error message"
        assert response.data["password"] == [
            "Ensure this value has at most 128 characters (it has 253)."
        ], "Unexpected password error message"

    def test_login_with_special_characters(
        self, not_authenticated_api_client: APIClient
    ):
        special_email = "special.user+test@example.com"
        special_password = "P@ss!w#rd$%"

        user = CustomUser.objects.create_user(
            email=special_email, password=special_password
        )

        response = not_authenticated_api_client.post(
            "/auth/token/login/", {"email": special_email, "password": special_password}
        )
        assert (
            response.status_code == status.HTTP_200_OK
        ), "Should allow login with special characters in email and password"
        assert "auth_token" in response.data

        user_exists = CustomUser.objects.filter(email=special_email).exists()
        assert user_exists, "User with special characters in email should be created"
        assert Token.objects.filter(
            user=user
        ).exists(), "Token should be created for user with special characters in email"


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
        response = authenticated_api_client.post(protected_url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.content


@pytest.mark.django_db
class TestPasswordReset:
    def test_request_password_reset(
        self, not_authenticated_api_client: APIClient, external_user: CustomUser
    ):
        url = "/auth/users/reset_password/"
        data = {"email": external_user.email}

        response = not_authenticated_api_client.post(url, data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT, response.content
        assert len(mail.outbox) == 1

        email = mail.outbox[0]
        assert email.subject == "Password reset on testserver"
        assert email.to == [external_user.email]
        assert "reset" in email.body

    def test_reset_password(
        self, not_authenticated_api_client: APIClient, external_user: CustomUser
    ):
        token_generator = PasswordResetTokenGenerator()
        reset_token = token_generator.make_token(external_user)

        reset_confirm_url = "/auth/users/reset_password_confirm/"
        uid = urlsafe_base64_encode(force_bytes(external_user.pk))
        data = {
            "uid": uid,
            "token": reset_token,
            "new_password": "newpassword123",
            "re_new_password": "newpassword123",
        }

        response = not_authenticated_api_client.post(reset_confirm_url, data=data)
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.content

    def test_login_with_new_password(
        self, not_authenticated_api_client: APIClient, external_user: CustomUser
    ):
        external_user.set_password("newpassword123")
        external_user.save()

        url = "/auth/token/login/"
        data = {"email": external_user.email, "password": "newpassword123"}

        response = not_authenticated_api_client.post(url, data=data)
        assert response.status_code == status.HTTP_200_OK, response.content


@pytest.mark.django_db
class TestPasswordChange:
    def test_password_change(
        self,
        authenticated_api_client: APIClient,
        authenticated_user: CustomUser,
        authenticated_user_password: str,
    ):
        assert authenticated_user.check_password(authenticated_user_password)

        change_password_url = "/auth/users/set_password/"
        data = {
            "current_password": authenticated_user_password,
            "new_password": "newpassword456",
            "re_new_password": "newpassword456",
        }
        response = authenticated_api_client.post(change_password_url, data=data)
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.content

        authenticated_user.refresh_from_db()
        assert authenticated_user.check_password("newpassword456")


@pytest.mark.django_db
class TestSecurity:
    def test_brute_force_login_limit_and_cooldown(
        self, not_authenticated_api_client: APIClient
    ):
        cache.clear()
        AccessAttempt.objects.all().delete()
        AccessLog.objects.all().delete()
        wrong_credentials = {
            "email": "testuser@example.com",
            "password": "wrongpassword",
        }

        attempts_trigger_mechanism = 10

        for _ in range(attempts_trigger_mechanism):
            response = not_authenticated_api_client.post(
                "/auth/token/login/", data=wrong_credentials
            )

        assert (
            response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        ), response.content
        assert (
            "Account locked: too many login attempts. Please try again later."
            in response.content.decode()
        )

        with freeze_time(datetime.datetime.now() + datetime.timedelta(hours=1)):
            response = not_authenticated_api_client.post(
                "/auth/token/login/", data=wrong_credentials
            )

            assert response.status_code == status.HTTP_403_FORBIDDEN, response.content
            assert response.json() == {"non_field_errors": ["Incorrect Credentials"]}

    def test_rate_limit_and_cooldown(
        self, authenticated_api_client: APIClient, authenticated_user: CustomUser
    ):
        cache.clear()
        AccessAttempt.objects.all().delete()
        AccessLog.objects.all().delete()
        rate_limit = 10
        rate_limit_exceed = rate_limit + 1
        cooldown_period = datetime.timedelta(seconds=60)
        shopping_list_1 = ShoppingList.objects.create(
            name="Shopping List 1", user=authenticated_user
        )

        for _ in range(rate_limit_exceed):
            response = authenticated_api_client.get(
                f"/shoppinglist/{shopping_list_1.pk}/"
            )

        assert (
            response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        ), response.content
        assert response.json() == {
            "detail": "Request was throttled. Expected available in 60 seconds."
        }

        with freeze_time(datetime.datetime.now() + cooldown_period):
            response = authenticated_api_client.get(
                f"/shoppinglist/{shopping_list_1.pk}/"
            )

            assert response.status_code == status.HTTP_200_OK, response.content
