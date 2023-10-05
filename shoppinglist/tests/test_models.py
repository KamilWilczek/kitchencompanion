import pytest
from django.core.exceptions import ValidationError
from freezegun import freeze_time

from conftest import create_item, create_multiple_items, create_shopping_list
from shoppinglist.constants import ItemCategory, ItemUnit
from shoppinglist.models import Item, ShoppingList
from users.models import CustomUser


@pytest.mark.django_db
class TestShoppingList:
    def test_user_foreignkey_in_shoppinglist(self, authenticated_user: CustomUser):
        shopping_list_with_user = create_shopping_list(
            user=authenticated_user, name="List with user"
        )
        assert shopping_list_with_user.user == authenticated_user

        user_id = authenticated_user.id
        authenticated_user.delete()

        with pytest.raises(ShoppingList.DoesNotExist):
            ShoppingList.objects.get(user_id=user_id)

    def test_shoppinglist_without_user(self):
        shopping_list_without_user = create_shopping_list(name="List without user")
        assert shopping_list_without_user.user is None

    def test_shopping_list_and_item_creation(self, shopping_list):
        assert shopping_list.name == "Test List"

        item = create_item(shopping_list=shopping_list, quantity=12)

        assert item.product == "Milk"
        assert item.quantity == 12
        assert item.category == ItemCategory.DAIRY

        assert item.completed == False

        items_linked_to_list = shopping_list.items.all()

        assert len(items_linked_to_list) == 1
        assert items_linked_to_list[0].product == "Milk"

    def test_shoppinglist_name_field(self, shopping_list):
        retrieved_list = ShoppingList.objects.get(pk=shopping_list.pk)

        assert retrieved_list.name == "Test List"
        assert ShoppingList._meta.get_field("name").max_length == 220

    def test_shoppinglist_description_field(self, shopping_list):
        shopping_list.description = "My Shopping List Description"
        shopping_list.save()

        retrieved_list = ShoppingList.objects.get(pk=shopping_list.pk)

        assert retrieved_list.description == "My Shopping List Description"

    def test_items_deleted_with_shopping_list(self, shopping_list):
        items_data = [
            {"product": "Milk", "category": ItemCategory.DAIRY},
            {"product": "Bread", "category": ItemCategory.BREAD},
            {"product": "Apples", "category": ItemCategory.FRUITS_VEGETABLES},
        ]

        create_multiple_items(shopping_list, items_data)

        assert Item.objects.filter(shopping_list=shopping_list).count() == 3

        shopping_list_id = shopping_list.id

        shopping_list.delete()

        assert Item.objects.filter(shopping_list_id=shopping_list_id).count() == 0

    def test_shoppinglist_str_representation(self, shopping_list):
        assert str(shopping_list) == "Test List"


@pytest.mark.django_db
class TestItem:
    def test_item_product_field(self, shopping_list):
        item = create_item(shopping_list=shopping_list)
        retrieved_item = Item.objects.get(pk=item.pk)

        assert retrieved_item.product == "Milk"
        assert Item._meta.get_field("product").max_length == 200

    def test_item_unit_category_choices(self, shopping_list):
        item = create_item(
            shopping_list=shopping_list,
            unit=ItemUnit.LITER,
        )

        retrieved_item = Item.objects.get(pk=item.pk)

        assert retrieved_item.category == ItemCategory.DAIRY
        assert retrieved_item.unit == ItemUnit.LITER
        assert ItemUnit.LITER.value in dict(Item._meta.get_field("unit").flatchoices)

    def test_item_ordering_by_completed(self, shopping_list):
        items_data = [
            {"product": "Milk", "category": ItemCategory.DAIRY, "completed": True},
            {"product": "Bread", "category": ItemCategory.BREAD, "completed": False},
            {
                "product": "Apples",
                "category": ItemCategory.FRUITS_VEGETABLES,
                "completed": True,
            },
        ]

        create_multiple_items(shopping_list, items_data)

        items_from_db = list(Item.objects.all())

        assert items_from_db[0].product == "Bread"
        assert items_from_db[1].product in ["Milk", "Apples"]
        assert items_from_db[2].product in ["Milk", "Apples"]
        assert items_from_db[1].product != items_from_db[2].product

    def test_item_additional_notes(self, shopping_list):
        item_note = "This is a note for testing purposes."
        item_with_note = create_item(
            shopping_list=shopping_list,
            note=item_note,
        )

        retrieved_item = Item.objects.get(pk=item_with_note.pk)
        assert retrieved_item.note == item_note

    def test_timestamps(self, shopping_list):
        with freeze_time("2022-01-01 12:00:00"):
            item = create_item(
                shopping_list=shopping_list,
                quantity=12,
            )

            initial_created = item.created
            initial_updated = item.updated

        with freeze_time("2022-01-01 14:00:00"):
            item.product = "Updated Test Product"
            item.save()

            updated_item = Item.objects.get(pk=item.pk)

            assert initial_created == updated_item.created
            assert initial_updated < updated_item.updated

    def test_text_fields_max_length(self, shopping_list):
        max_length_product = Item._meta.get_field("product").max_length
        assert max_length_product == 200

        item_with_too_long_product = create_item(
            shopping_list=shopping_list,
            product="P" * (max_length_product + 1),
        )
        with pytest.raises(
            ValidationError, match="Ensure this value has at most 200 characters"
        ):
            item_with_too_long_product.full_clean()

    @pytest.mark.parametrize("quantity", [-1, 0])
    def test_invalid_quantity_raises_validation_error(self, quantity, shopping_list):
        item = Item(
            shopping_list=shopping_list,
            product="Test Product",
            quantity=quantity,
            category=ItemCategory.DAIRY,
        )
        with pytest.raises(
            ValidationError, match="Ensure this value is greater than or equal to 1."
        ):
            item.full_clean()

    def test_updating_to_invalid_quantity_raises_validation_error(self, shopping_list):
        valid_item = create_item(
            shopping_list=shopping_list,
            quantity=10,
        )
        valid_item.quantity = -5
        with pytest.raises(
            ValidationError, match="Ensure this value is greater than or equal to 1."
        ):
            valid_item.full_clean()

        valid_item.quantity = 0
        with pytest.raises(
            ValidationError, match="Ensure this value is greater than or equal to 1."
        ):
            valid_item.full_clean()

    def test_enum_choices_in_item(self, shopping_list):
        item_with_invalid_unit = create_item(
            shopping_list=shopping_list,
            product="Invalid Unit Product",
            unit="invalid_unit",
        )
        with pytest.raises(
            ValidationError, match="Value 'invalid_unit' is not a valid choice"
        ):
            item_with_invalid_unit.full_clean()

        item_with_invalid_category = create_item(
            shopping_list=shopping_list,
            product="Invalid Category Product",
            unit=ItemUnit.LITER,
            category="invalid_category",
        )
        with pytest.raises(
            ValidationError, match="Value 'invalid_category' is not a valid choice"
        ):
            item_with_invalid_category.full_clean()

    def test_item_str_representation(self, shopping_list):
        item = create_item(
            shopping_list=shopping_list,
            quantity=12,
        )
        assert str(item) == "Milk"
