import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestIsAuthenticated:
    def test_protected_endpoint_without_auth(
        self, not_authenticated_api_client: APIClient
    ):
        response = not_authenticated_api_client.get("/logout/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_protected_endpoint_with_invalid_token(
        self, authenticated_api_client: APIClient
    ):
        # Overwrite the token with an invalid one
        authenticated_api_client.credentials(
            HTTP_AUTHORIZATION="Token " + "invalid_token_string"
        )

        response = authenticated_api_client.get("/logout/")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
