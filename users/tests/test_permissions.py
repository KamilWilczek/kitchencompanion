import pytest
from rest_framework import status
from rest_framework.test import APIClient

from users.models import CustomUser


@pytest.mark.django_db
class TestIsAuthenticated:
    def test_protected_endpoint_without_auth(
        self, not_authenticated_api_client: APIClient
    ):
        response = not_authenticated_api_client.get("/auth/token/logout/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_protected_endpoint_with_invalid_token(
        self, authenticated_api_client: APIClient
    ):
        authenticated_api_client.credentials(
            HTTP_AUTHORIZATION="Token " + "invalid_token_string"
        )

        response = authenticated_api_client.get("/auth/token/logout/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_while_authenticated(
        self, authenticated_api_client: APIClient, authenticated_user: CustomUser
    ):
        response = authenticated_api_client.post(
            "/auth/token/login/",
            {
                "email": authenticated_user.email,
                "password": authenticated_user.password,
            },
        )

        assert (
            response.status_code == status.HTTP_403_FORBIDDEN
        ), "Authenticated user should not be able to access login endpoint"

    def test_register_while_authenticated(
        self, authenticated_api_client: APIClient, authenticated_user: CustomUser
    ):
        response = authenticated_api_client.post(
            "/auth/users/",
            {
                "email": authenticated_user.email,
                "password": authenticated_user.password,
            },
        )

        assert (
            response.status_code == status.HTTP_400_BAD_REQUEST
        ), "Authenticated user should not be able to access register endpoint"
