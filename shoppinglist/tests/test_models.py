import time
import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from shoppinglist.models import ShoppingList, Item
from shoppinglist.constants import ItemCategory, ItemUnit


def create_user():
    return User.objects.create_user(username="testuser", password="testpassword")


def create_shopping_list(name="Test List", user=None):
    return ShoppingList.objects.create(name=name, user=user)


def create_item(
    shopping_list, product="Test Product", category=ItemCategory.DAIRY, **kwargs
):
    return Item.objects.create(
        shopping_list=shopping_list, product=product, category=category, **kwargs
    )


@pytest.fixture
def user():
    return create_user()


@pytest.fixture
def shopping_list(user):
    return create_shopping_list(user=user)


class TestShoppingList:
    @pytest.mark.django_db
    def test_shopping_list_and_item_creation(self, shopping_list):
        assert shopping_list.name == "Test List"

        item = create_item(shopping_list=shopping_list, quantity=12)

        assert item.product == "Test Product"
        assert item.quantity == 12
        assert item.category == ItemCategory.DAIRY

        assert item.completed == False

        items_linked_to_list = shopping_list.item.all()

        assert len(items_linked_to_list) == 1
        assert items_linked_to_list[0].product == "Test Product"

    @pytest.mark.django_db
    def test_shoppinglist_name_field(self, shopping_list):
        retrieved_list = ShoppingList.objects.get(id=shopping_list.id)

        assert retrieved_list.name == "Test List"
        assert ShoppingList._meta.get_field("name").max_length == 220

    @pytest.mark.django_db
    def test_shoppinglist_description_field(self, shopping_list):
        shopping_list.description = "My Shopping List Description"
        shopping_list.save()

        retrieved_list = ShoppingList.objects.get(id=shopping_list.id)

        assert retrieved_list.description == "My Shopping List Description"

    @pytest.mark.django_db
    def test_cascading_delete_of_items_when_shoppinglist_deleted(self, shopping_list):
        create_item(
            shopping_list=shopping_list, product="Milk", category=ItemCategory.DAIRY
        )
        create_item(
            shopping_list=shopping_list, product="Bread", category=ItemCategory.BREAD
        )
        create_item(
            shopping_list=shopping_list,
            product="Apples",
            category=ItemCategory.FRUITS_VEGETABLES,
        )

        assert Item.objects.filter(shopping_list=shopping_list).count() == 3

        shopping_list_id = shopping_list.id

        shopping_list.delete()

        assert Item.objects.filter(shopping_list_id=shopping_list_id).count() == 0

    @pytest.mark.django_db
    def test_user_foreignkey_in_shoppinglist(self, user):
        shopping_list_with_user = create_shopping_list(user=user, name="List with user")
        assert shopping_list_with_user.user == user

        shopping_list_without_user = create_shopping_list(name="List without user")
        assert shopping_list_without_user.user is None

        user_id = user.id
        user.delete()

        with pytest.raises(ShoppingList.DoesNotExist):
            ShoppingList.objects.get(user_id=user_id)

    @pytest.mark.django_db
    def test_shoppinglist_str_representation(self, shopping_list):
        assert str(shopping_list) == "Test List"


class TestItem:
    @pytest.mark.django_db
    def test_item_product_field(self, shopping_list):
        item = create_item(shopping_list=shopping_list)
        retrieved_item = Item.objects.get(id=item.id)

        assert retrieved_item.product == "Test Product"
        assert Item._meta.get_field("product").max_length == 200

    @pytest.mark.django_db
    def test_item_unit_category_choices(self, shopping_list):
        item = create_item(
            shopping_list=shopping_list,
            unit=ItemUnit.LITER,
        )

        retrieved_item = Item.objects.get(id=item.id)

        assert retrieved_item.category == ItemCategory.DAIRY
        assert retrieved_item.unit == ItemUnit.LITER
        assert ItemUnit.LITER.value in dict(Item._meta.get_field("unit").flatchoices)

    @pytest.mark.django_db
    def test_item_ordering_by_completed(self, shopping_list):
        item1 = create_item(
            shopping_list=shopping_list,
            product="Milk",
            category=ItemCategory.DAIRY,
            completed=True,
        )

        item2 = create_item(
            shopping_list=shopping_list,
            product="Bread",
            category=ItemCategory.BREAD,
            completed=False,
        )

        item3 = create_item(
            shopping_list=shopping_list,
            product="Apples",
            category=ItemCategory.FRUITS_VEGETABLES,
            completed=True,
        )

        items = list(Item.objects.all())

        assert items[0] == item2
        assert items[1] == item1 or items[1] == item3
        assert items[2] == item1 or items[2] == item3

    @pytest.mark.django_db
    def test_enum_choices_in_item(self, shopping_list):
        with pytest.raises(ValidationError):
            item_with_invalid_unit = create_item(
                shopping_list=shopping_list,
                product="Invalid Unit Product",
                unit="invalid_unit",
            )
            item_with_invalid_unit.full_clean()

        with pytest.raises(ValidationError):
            item_with_invalid_category = create_item(
                shopping_list=shopping_list,
                product="Invalid Category Product",
                unit=ItemUnit.LITER,
                category="invalid_category",
            )
            item_with_invalid_category.full_clean()

    @pytest.mark.django_db
    def test_positive_quantity_in_item(self, shopping_list):
        with transaction.atomic():
            with pytest.raises(IntegrityError):
                item_with_negative_quantity = create_item(
                    shopping_list=shopping_list,
                    quantity=-1,
                )
                item_with_negative_quantity.full_clean()

        with pytest.raises(ValidationError):
            item_with_zero_quantity = create_item(
                shopping_list=shopping_list,
                quantity=0,
            )
            item_with_zero_quantity.full_clean()

        valid_item = create_item(
            shopping_list=shopping_list,
            quantity=10,
        )

        valid_item.quantity = -5
        with pytest.raises(ValidationError):
            valid_item.full_clean()

        valid_item.quantity = 0
        with pytest.raises(ValidationError):
            valid_item.full_clean()

    @pytest.mark.django_db
    def test_item_additional_notes(self, shopping_list):
        item_note = "This is a note for testing purposes."
        item_with_note = create_item(
            shopping_list=shopping_list,
            note=item_note,
        )

        retrieved_item = Item.objects.get(pk=item_with_note.pk)
        assert retrieved_item.note == item_note

    @pytest.mark.django_db
    def test_item_str_representation(self, shopping_list):
        item = create_item(
            shopping_list=shopping_list,
            quantity=12,
        )
        assert str(item) == "Test Product"

    @pytest.mark.django_db
    def test_timestamps(self, shopping_list):
        item = create_item(
            shopping_list=shopping_list,
            quantity=12,
        )

        initial_created = item.created
        initial_updated = item.updated

        time.sleep(2)

        item.product = "Updated Test Product"
        item.save()

        updated_item = Item.objects.get(pk=item.pk)

        assert initial_created == updated_item.created
        assert initial_updated < updated_item.updated

    @pytest.mark.django_db
    def test_text_fields_max_length(self, shopping_list):
        max_length_product = Item._meta.get_field("product").max_length

        assert max_length_product == 200

        with pytest.raises(ValidationError):
            item_with_too_long_product = create_item(
                shopping_list=shopping_list,
                product="P" * (max_length_product + 1),
            )
            item_with_too_long_product.full_clean()
