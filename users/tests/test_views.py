from typing import Dict

import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.models import CustomUser


@pytest.mark.django_db
class TestRegisterView:
    def test_register_user(self, not_authenticated_api_client: APIClient):
        url = "/register/"
        data: Dict[str, str] = {
            "email": "notregistereduser@example.com",
            "password": "notregistereduserpassword",
        }
        response = not_authenticated_api_client.post(url, data)

        assert response.status_code == 201, response.content
        assert CustomUser.objects.filter(email="notregistereduser@example.com").exists()


@pytest.mark.django_db
class TestLoginView:
    def test_login_user(
        self,
        not_authenticated_api_client: APIClient,
        external_user: CustomUser,
        external_user_password: str,
    ):
        url = "/login/"
        data: Dict[str, str] = {
            "email": external_user.email,
            "password": external_user_password,
        }

        response = not_authenticated_api_client.post(url, data)

        assert response.status_code == 200, response.content
        assert "token" in response.data

        user = CustomUser.objects.get(email=external_user.email)
        assert Token.objects.filter(user=user).exists()


@pytest.mark.django_db
class TestLogoutView:
    def test_logout_user(self, authenticated_api_client: APIClient):
        url = "/logout/"

        response = authenticated_api_client.post(url)

        assert response.status_code == 200, response.content

        user = CustomUser.objects.get(email="testuser@example.com")
        assert not Token.objects.filter(user=user).exists()


@pytest.mark.django_db
class TestDeleteAccountView:
    def test_delete_account(
        self, authenticated_api_client: APIClient, authenticated_user: CustomUser
    ):
        url = f"/delete_account/"

        response = authenticated_api_client.delete(url)

        assert response.status_code == 204, response.content
        assert not CustomUser.objects.filter(pk=authenticated_user.pk).exists()
