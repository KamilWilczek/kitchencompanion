import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from shoppinglist.models import ShoppingList


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpassword")


def create_shopping_list(name="Test List", user=None):
    return ShoppingList.objects.create(name=name, user=user)


class TestShoppingListView:
    @pytest.mark.django_db
    def test_all_shopping_lists_are_returned(self, user):
        shopping_list_1 = create_shopping_list(name="Shopping List 1", user=user)
        shopping_list_2 = create_shopping_list(name="Shopping List 2", user=user)
        shopping_list_3 = create_shopping_list(name="Shopping List 3", user=user)

        client = APIClient()
        response = client.get("/shoppinglist/")

        assert response.status_code == 200
        assert len(response.data) == 3
