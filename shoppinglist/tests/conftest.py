from typing import Any, Dict, List, Union

import pytest
from rest_framework.test import APIClient

from shoppinglist.constants import ItemCategory
from shoppinglist.models import Item, ShoppingList
from users.models import CustomUser


@pytest.fixture
def not_authenticated_api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def authenticated_api_client(user: CustomUser) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def user() -> CustomUser:
    return CustomUser.objects.create_user(
        email="testuser@example.com",
        password="testpassword",
    )


@pytest.fixture
def test_user() -> CustomUser:
    return CustomUser.objects.create_user(
        email="testuser@gmail.com", password="testuserpassword"
    )


@pytest.fixture
def shopping_list(user: CustomUser) -> ShoppingList:
    return create_shopping_list(user=user)


def create_shopping_list(
    name: str = "Test List", user: Union[CustomUser, None] = None
) -> ShoppingList:
    return ShoppingList.objects.create(name=name, user=user)


def create_item(
    shopping_list: ShoppingList,
    product: str = "Milk",
    category: ItemCategory = ItemCategory.DAIRY,
    **kwargs: Any
) -> Item:
    return Item.objects.create(
        shopping_list=shopping_list, product=product, category=category, **kwargs
    )


def create_multiple_items(
    shopping_list: ShoppingList, items_data: List[Dict[str, Any]]
) -> None:
    items_to_create = [Item(shopping_list=shopping_list, **data) for data in items_data]
    Item.objects.bulk_create(items_to_create)
