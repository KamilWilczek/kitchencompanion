import pytest
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.models import CustomUser
from users.serializers import LoginSerializer, RegisterSerializer


@pytest.mark.django_db
class TestRegisterView:
    def test_register_user(self, not_authenticated_api_client):
        url = "/register/"
        data = {"email": "test2@example.com", "password": "testpassword2"}
        response = not_authenticated_api_client.post(url, data)
        assert response.status_code == 201
        assert CustomUser.objects.filter(email="test2@example.com").exists()


@pytest.mark.django_db
class TestLoginView:
    def test_login_user(self, not_authenticated_api_client):
        url = "/login/"
        data = {"email": "testuser@example.com", "password": "testpassword"}
        response = not_authenticated_api_client.post(url, data)
        assert response.status_code == 200
        assert "token" in response.data
        user = CustomUser.objects.get(email="testuser@example.com")
        assert Token.objects.filter(user=user).exists()


@pytest.mark.django_db
class TestLogoutView:
    def test_logout_user(self, authenticated_api_client):
        url = "/logout/"
        response = authenticated_api_client.post(url)
        assert response.status_code == 200
        # Token should be deleted after logout
        user = CustomUser.objects.get(email="testuser@example.com")
        assert not Token.objects.filter(user=user).exists()


@pytest.mark.django_db
class TestDeleteAccountView:
    def test_delete_account(self, authenticated_api_client, authenticated_user):
        url = f"/delete_account/"
        response = authenticated_api_client.delete(url)
        assert response.status_code == 204
        assert not CustomUser.objects.filter(pk=authenticated_user.pk).exists()
