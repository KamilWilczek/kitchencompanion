import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from shoppinglist.constants import ItemCategory
from shoppinglist.models import Item, ShoppingList


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def shopping_list(user):
    return create_shopping_list(user=user)


def create_shopping_list(name="Test List", user=None):
    return ShoppingList.objects.create(name=name, user=user)


def create_item(shopping_list, product="Milk", category=ItemCategory.DAIRY, **kwargs):
    return Item.objects.create(
        shopping_list=shopping_list, product=product, category=category, **kwargs
    )


def create_multiple_items(shopping_list, items_data):
    items_to_create = [Item(shopping_list=shopping_list, **data) for data in items_data]
    Item.objects.bulk_create(items_to_create)
