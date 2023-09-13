from typing import Any, Dict, List, Union

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from shoppinglist.constants import ItemCategory
from shoppinglist.models import Item, ShoppingList


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user() -> User:
    return User.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def shopping_list(user: User) -> ShoppingList:
    return create_shopping_list(user=user)


def create_shopping_list(
    name: str = "Test List", user: Union[User, None] = None
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
