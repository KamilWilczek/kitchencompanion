import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient
from shoppinglist.models import ShoppingList, Item
from shoppinglist.constants import ItemCategory


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpassword")


def create_shopping_list(name="Test List", user=None):
    return ShoppingList.objects.create(name=name, user=user)


def create_multiple_items(shopping_list, items_data):
    items_to_create = [Item(shopping_list=shopping_list, **data) for data in items_data]
    Item.objects.bulk_create(items_to_create)


class TestShoppingListView:
    @pytest.mark.django_db
    def test_all_shopping_lists_are_returned(self, user):
        shopping_list_1 = create_shopping_list(name="Shopping List 1", user=user)
        shopping_list_2 = create_shopping_list(name="Shopping List 2", user=user)
        shopping_list_3 = create_shopping_list(name="Shopping List 3", user=user)

        client = APIClient()
        response = client.get("/shoppinglist/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    @pytest.mark.django_db
    def test_items_count_returns_correct_number(self, user):
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

        client = APIClient()
        response = client.get("/shoppinglist/")

        assert response.status_code == status.HTTP_200_OK, response.content
        assert response.data[0]["items_count"] == 3
        assert response.data[1]["items_count"] == 2


class TestShoppingListCreateView:
    @pytest.mark.django_db
    def test_create_shopping_list(self, user):
        client = APIClient()

        data = {
            "name": "Shopping List",
            "user": user.id,
        }

        response = client.post("/shoppinglist/create/", data=data)

        assert response.status_code == status.HTTP_201_CREATED, response.content
        assert response.data["name"] == data["name"]
        assert ShoppingList.objects.filter(name=data["name"]).exists()

    @pytest.mark.django_db
    def test_create_shopping_list_missing_required_fields(self, user):
        client = APIClient()

        data = {
            "user": user.id,
            "description": "Groceries",
        }

        response = client.post("/shoppinglist/create/", data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
        assert response.data == {"name": ["This field is required."]}

    @pytest.mark.django_db
    def test_create_shopping_list_with_invalid_data_types(self, user):
        client = APIClient()

        data = {
            "user": "invalid_user_id",
            "name": 12345,
            "description": 67890,
            "completed": "true_string",
        }

        response = client.post("/shoppinglist/create/", data=data)

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
