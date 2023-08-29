import time
import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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


@pytest.mark.django_db
def test_shopping_list_and_item_creation(shopping_list):
    shopping_list = shopping_list

    assert shopping_list.name == "Test List"

    item = Item.objects.create(
        shopping_list=shopping_list,
        product="Eggs",
        quantity=12,
        category=ItemCategory.DAIRY,
    )

    assert item.product == "Eggs"
    assert item.quantity == 12
    assert item.category == ItemCategory.DAIRY

    assert item.completed == False

    items_linked_to_list = shopping_list.item.all()

    assert len(items_linked_to_list) == 1
    assert items_linked_to_list[0].product == "Eggs"


@pytest.mark.django_db
def test_shoppinglist_name_field():
    shop_list = ShoppingList(name="My List")
    shop_list.save()
    retrieved_list = ShoppingList.objects.get(id=shop_list.id)

    assert retrieved_list.name == "My List"
    assert ShoppingList._meta.get_field("name").max_length == 220


@pytest.mark.django_db
def test_shoppinglist_description_field():
    shop_list = ShoppingList(name="List", description="My Shopping List Description")
    shop_list.save()
    retrieved_list = ShoppingList.objects.get(id=shop_list.id)

    assert retrieved_list.description == "My Shopping List Description"


@pytest.mark.django_db
def test_cascading_delete_of_items_when_shoppinglist_deleted():
    shopping_list = ShoppingList.objects.create(name="Deletion Test List")

    Item.objects.create(
        shopping_list=shopping_list, product="Milk", category=ItemCategory.DAIRY
    )

    Item.objects.create(
        shopping_list=shopping_list, product="Bread", category=ItemCategory.BREAD
    )

    Item.objects.create(
        shopping_list=shopping_list,
        product="Apples",
        category=ItemCategory.FRUITS_VEGETABLES,
    )

    assert Item.objects.filter(shopping_list=shopping_list).count() == 3

    shopping_list_id = shopping_list.id

    shopping_list.delete()

    assert Item.objects.filter(shopping_list_id=shopping_list_id).count() == 0


@pytest.mark.django_db
def test_user_foreignkey_in_shoppinglist(user):
    shopping_list_with_user = create_shopping_list(user=user, name="List with user")
    assert shopping_list_with_user.user == user

    shopping_list_without_user = create_shopping_list(name="List without user")
    assert shopping_list_without_user.user is None

    user_id = user.id
    user.delete()

    with pytest.raises(ShoppingList.DoesNotExist):
        ShoppingList.objects.get(user_id=user_id)


@pytest.mark.django_db
def test_shoppinglist_str_representation():
    shop_list = ShoppingList.objects.create(name="Weekly Groceries")
    assert str(shop_list) == "Weekly Groceries"


@pytest.mark.django_db
def test_item_product_field():
    shop_list = ShoppingList(name="My List")
    shop_list.save()
    item = Item(shopping_list=shop_list, product="Milk", category=ItemCategory.DAIRY)
    item.save()
    retrieved_item = Item.objects.get(id=item.id)

    assert retrieved_item.product == "Milk"
    assert Item._meta.get_field("product").max_length == 200


@pytest.mark.django_db
def test_item_unit_choices():
    shop_list = ShoppingList(name="My List")
    shop_list.save()
    item = Item(
        shopping_list=shop_list,
        product="Milk",
        unit=ItemUnit.LITER,
        category=ItemCategory.DAIRY,
    )
    item.save()
    retrieved_item = Item.objects.get(id=item.id)

    assert retrieved_item.unit == ItemUnit.LITER
    assert ItemUnit.LITER.value in dict(Item._meta.get_field("unit").flatchoices)


@pytest.mark.django_db
def test_item_ordering_by_completed():
    shopping_list = ShoppingList.objects.create(name="Ordering Test List")

    item1 = Item.objects.create(
        shopping_list=shopping_list,
        product="Milk",
        category=ItemCategory.DAIRY,
        completed=True,
    )

    item2 = Item.objects.create(
        shopping_list=shopping_list,
        product="Bread",
        category=ItemCategory.BREAD,
        completed=False,
    )

    item3 = Item.objects.create(
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
def test_enum_choices_in_item():
    shopping_list = ShoppingList.objects.create(name="Test List")

    with pytest.raises(ValidationError):
        item_with_invalid_unit = Item(
            shopping_list=shopping_list,
            product="Invalid Unit Product",
            unit="invalid_unit",
            category=ItemCategory.DAIRY,
        )
        item_with_invalid_unit.full_clean()

    with pytest.raises(ValidationError):
        item_with_invalid_category = Item(
            shopping_list=shopping_list,
            product="Invalid Category Product",
            unit=ItemUnit.LITER,
            category="invalid_category",
        )
        item_with_invalid_category.full_clean()


@pytest.mark.django_db
def test_positive_quantity_in_item():
    shopping_list = ShoppingList.objects.create(name="Test List")

    with pytest.raises(ValidationError):
        item_with_negative_quantity = Item(
            shopping_list=shopping_list,
            product="Negative Quantity Product",
            quantity=-1,
            category=ItemCategory.DAIRY,
        )
        item_with_negative_quantity.full_clean()

    with pytest.raises(ValidationError):
        item_with_zero_quantity = Item(
            shopping_list=shopping_list,
            product="Zero Quantity Product",
            quantity=0,
            category=ItemCategory.DAIRY,
        )
        item_with_zero_quantity.full_clean()

    valid_item = Item.objects.create(
        shopping_list=shopping_list,
        product="Valid Product",
        quantity=10,
        category=ItemCategory.DAIRY,
    )

    valid_item.quantity = -5
    with pytest.raises(ValidationError):
        valid_item.full_clean()

    valid_item.quantity = 0
    with pytest.raises(ValidationError):
        valid_item.full_clean()


@pytest.mark.django_db
def test_item_additional_notes():
    shopping_list = ShoppingList.objects.create(name="Test List")

    item_note = "This is a note for testing purposes."
    item_with_note = Item.objects.create(
        shopping_list=shopping_list,
        product="Product with Note",
        category=ItemCategory.DAIRY,
        note=item_note,
    )

    retrieved_item = Item.objects.get(pk=item_with_note.pk)
    assert retrieved_item.note == item_note


@pytest.mark.django_db
def test_item_str_representation():
    shopping_list = ShoppingList.objects.create(name="My Shopping List")
    item = Item.objects.create(
        shopping_list=shopping_list,
        product="Eggs",
        quantity=12,
        category=ItemCategory.DAIRY,
    )
    assert str(item) == "Eggs"


@pytest.mark.django_db
def test_timestamps():
    shopping_list = ShoppingList.objects.create(name="My Shopping List")

    item = Item.objects.create(
        shopping_list=shopping_list,
        product="Eggs",
        quantity=12,
        category=ItemCategory.DAIRY,
    )

    initial_created = item.created
    initial_updated = item.updated

    time.sleep(2)

    item.product = "Updated Eggs"
    item.save()

    updated_item = Item.objects.get(pk=item.pk)

    assert initial_created == updated_item.created
    assert initial_updated < updated_item.updated


@pytest.mark.django_db
def test_text_fields_max_length():
    shopping_list = ShoppingList.objects.create(name="Test List")

    max_length_product = Item._meta.get_field("product").max_length

    assert max_length_product == 200

    with pytest.raises(ValidationError):
        item_with_too_long_product = Item(
            shopping_list=shopping_list,
            product="P" * (max_length_product + 1),
            category=ItemCategory.DAIRY,
        )
        item_with_too_long_product.full_clean()
