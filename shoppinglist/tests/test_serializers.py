import pytest
from shoppinglist.serializers import ItemSerializer, ShoppingListSerializer
from shoppinglist.constants import ItemCategory, ItemUnit
from .error_messages import ERRORS
from .conftest import create_item


class TestShoppingListSerializer:
    @pytest.mark.django_db
    def test_shopping_list_serializer_valid_data(self, user):
        data = {
            "user": user.id,
            "name": "Test Shopping List",
            "description": "This is test shopping list",
            "completed": False,
            "items_count": 0,
        }
        serializer = ShoppingListSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.data == data

    @pytest.mark.parametrize(
        "data, expected_errors",
        [
            (
                {
                    "user": "invalid_user_id",
                    "name": "valid name",
                    "completed": "true_string",
                },
                {
                    "user": [ERRORS.INCORRECT_TYPE_ERROR],
                    "completed": [ERRORS.INVALID_BOOLEAN_ERROR],
                },
            ),
        ],
    )
    def test_shopping_list_serializer_invalid_data(self, data, expected_errors):
        serializer = ShoppingListSerializer(data=data)
        assert not serializer.is_valid()
        assert serializer.errors == expected_errors

    @pytest.mark.django_db
    def test_items_and_items_count_fields(self, shopping_list):
        create_item(
            shopping_list=shopping_list, quantity=1, note="Test Note 1", completed=False
        )
        create_item(
            shopping_list=shopping_list,
            product="Beef",
            quantity=2,
            note="Test Note 2",
            category=ItemCategory.MEAT,
            completed=True,
        )

        serializer = ShoppingListSerializer(shopping_list)

        assert len(serializer.data["items"]) == 2
        assert serializer.data["items_count"] == 2

        assert serializer.data["items"][0]["product"] == "Milk"
        assert serializer.data["items"][1]["product"] == "Beef"


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
        assert serializer.data == data

    @pytest.mark.parametrize(
        "data, expected_errors",
        [
            (
                {
                    "product": "Milk",
                    "quantity": -1,
                    "unit": "invalid_unit",
                    "category": 123,
                    "completed": "true_string",
                },
                {
                    "quantity": [ERRORS.MIN_QUANTITY_ERROR],
                    "unit": [ERRORS.INVALID_CHOICE_ERROR_UNIT],
                    "category": [ERRORS.INVALID_CHOICE_ERROR_CATEGORY],
                    "completed": [ERRORS.INVALID_BOOLEAN_ERROR],
                },
            ),
        ],
    )
    def test_item_serializer_invalid_data(self, data, expected_errors):
        serializer = ItemSerializer(data=data)
        assert not serializer.is_valid()
        assert serializer.errors == expected_errors
