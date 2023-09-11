import pytest
from shoppinglist.serializers import ItemSerializer, ShoppingListSerializer
from shoppinglist.constants import ItemCategory, ItemUnit


class TestShoppingListSerializer:
    @pytest.mark.django_db
    def test_shopping_list_serializer_valid_data(self, user):
        data = {
            "user": user.id,
            "name": "Test Shopping List",
            "description": "This is test shopping list",
            "completed": False,
        }
        serializer = ShoppingListSerializer(data=data)
        assert serializer.is_valid()

    def test_shopping_list_serializer_invalid_data(self):
        data = {
            "user": "invalid_user_id",
            "name": 12345,
            "description": 67890,
            "completed": "true_string",
        }
        serializer = ShoppingListSerializer(data=data)
        assert not serializer.is_valid()


class TestItemSerializer:
    def test_item_serializer_valid_data(self):
        data = {
            "product": "Test Product",
            "quantity": 2,
            "unit": ItemUnit.KILOGRAM,
            "note": "Test Note",
            "category": ItemCategory.DAIRY,
            "completed": False,
        }
        serializer = ItemSerializer(data=data)
        assert serializer.is_valid()

    def test_item_serializer_invalid_data(self):
        data = {
            "product": "Milk",
            "quantity": -1,
            "unit": "invalid_unit",
            "category": 123,
            "completed": "true_string",
        }
        serializer = ItemSerializer(data=data)
        assert not serializer.is_valid()
