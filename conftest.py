from typing import Any, Dict, List

import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from shoppinglist.constants import ItemCategory
from shoppinglist.models import Item, ShoppingList
from users.models import CustomUser


@pytest.fixture
def not_authenticated_api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def authenticated_api_client(authenticated_user: CustomUser) -> APIClient:
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=authenticated_user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client


@pytest.fixture
def authenticated_user_password() -> str:
    return "testpassword"


@pytest.fixture
def authenticated_user(authenticated_user_password: str) -> CustomUser:
    return CustomUser.objects.create_user(
        email="testuser@example.com",
        password=authenticated_user_password,
    )


@pytest.fixture
def external_user_password() -> str:
    return "externalpassword"


@pytest.fixture
def external_user(external_user_password: str) -> CustomUser:
    return CustomUser.objects.create_user(
        email="externaluser@example.com",
        password=external_user_password,
    )


@pytest.fixture
def third_user() -> CustomUser:
    return CustomUser.objects.create_user(
        email="thirduser@example.com",
        password="thirdpassword",
    )


@pytest.fixture
def shopping_list(authenticated_user: CustomUser) -> ShoppingList:
    return create_shopping_list(user=authenticated_user)


def create_shopping_list(
    name: str = "Test List", user: CustomUser | None = None
) -> ShoppingList:
    return ShoppingList.objects.create(name=name, user=user)


def create_item(
    shopping_list: ShoppingList,
    product: str = "Milk",
    category: ItemCategory = ItemCategory.DAIRY,
    **kwargs: Any,
) -> Item:
    return Item.objects.create(
        shopping_list=shopping_list, product=product, category=category, **kwargs
    )


def create_multiple_items(
    shopping_list: ShoppingList, items_data: List[Dict[str, Any]]
) -> None:
    items_to_create = [Item(shopping_list=shopping_list, **data) for data in items_data]
    Item.objects.bulk_create(items_to_create)
