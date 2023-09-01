import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient
from shoppinglist.models import ShoppingList, Item
from shoppinglist.constants import ItemCategory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpassword")


def create_shopping_list(name="Test List", user=None):
    return ShoppingList.objects.create(name=name, user=user)


def create_multiple_items(shopping_list, items_data):
    items_to_create = [Item(shopping_list=shopping_list, **data) for data in items_data]
    Item.objects.bulk_create(items_to_create)


@pytest.mark.django_db
class TestShoppingListView:
    def test_all_shopping_lists_are_returned(self, user, api_client):
        shopping_list_1 = create_shopping_list(name="Shopping List 1", user=user)
        shopping_list_2 = create_shopping_list(name="Shopping List 2", user=user)
        shopping_list_3 = create_shopping_list(name="Shopping List 3", user=user)

        response = api_client.get("/shoppinglist/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_items_count_returns_correct_number(self, user, api_client):
        shopping_list_1 = create_shopping_list(name="Shopping List 1", user=user)
        shopping_list_2 = create_shopping_list(name="Shopping List 2", user=user)
        items_data_1 = [
            {"product": "Milk", "category": ItemCategory.DAIRY},
            {"product": "Bread", "category": ItemCategory.BREAD},
            {"product": "Apples", "category": ItemCategory.FRUITS_VEGETABLES},
        ]
        items_data_2 = [
            {"product": "Beef", "category": ItemCategory.MEAT},
            {"product": "Butter", "category": ItemCategory.FATS},
        ]

        create_multiple_items(shopping_list_1, items_data_1)
        create_multiple_items(shopping_list_2, items_data_2)

        response = api_client.get("/shoppinglist/")

        assert response.status_code == status.HTTP_200_OK, response.content
        assert response.data[0]["items_count"] == 3
        assert response.data[1]["items_count"] == 2


@pytest.mark.django_db
class TestShoppingListCreateView:
    def test_create_shopping_list(self, user, api_client):
        data = {
            "name": "Shopping List",
            "user": user.id,
        }

        response = api_client.post("/shoppinglist/create/", data=data)

        assert response.status_code == status.HTTP_201_CREATED, response.content
        assert response.data["name"] == data["name"]
        assert ShoppingList.objects.filter(name=data["name"]).exists()

    def test_create_shopping_list_missing_required_fields(self, user, api_client):
        data = {
            "user": user.id,
            "description": "Groceries",
        }

        response = api_client.post("/shoppinglist/create/", data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
        assert response.data == {"name": ["This field is required."]}

    def test_create_shopping_list_with_invalid_data_types(self, api_client):
        data = {
            "user": "invalid_user_id",
            "name": 12345,
            "description": 67890,
            "completed": "true_string",
        }

        response = api_client.post("/shoppinglist/create/", data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
        assert response.data == {
            "user": [
                ErrorDetail(
                    string="Incorrect type. Expected pk value, received str.",
                    code="incorrect_type",
                )
            ],
            "completed": [
                ErrorDetail(string="Must be a valid boolean.", code="invalid")
            ],
        }


class TestShoppingListDetailUpdateView:
    @pytest.mark.django_db
    def test_retrieve_shopping_list_by_id(self, user, api_client):
        shopping_list = create_shopping_list(name="Shopping List", user=user)

        response = api_client.get(f"/shoppinglist/{shopping_list.pk}/edit/")

        assert response.status_code == status.HTTP_200_OK, response.content
        assert response.data["name"] == shopping_list.name

    @pytest.mark.django_db
    def test_update_shopping_list_by_id(self, user, api_client):
        shopping_list = create_shopping_list(name="Shopping List", user=user)

        data = {
            "name": "Test List",
        }

        response = api_client.put(f"/shoppinglist/{shopping_list.pk}/edit/", data=data)

        assert response.status_code == status.HTTP_200_OK, response.content
        assert response.data["name"] == data["name"]

    @pytest.mark.django_db
    def test_update_shopping_list_with_invalid_data(self, user, api_client):
        shopping_list = create_shopping_list(name="Shopping List", user=user)

        data = {
            "name": "Shopping List",
            "completed": "true_string",
        }

        response = api_client.put(f"/shoppinglist/{shopping_list.pk}/edit/", data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
        assert response.data == {
            "completed": [
                ErrorDetail(string="Must be a valid boolean.", code="invalid")
            ]
        }
