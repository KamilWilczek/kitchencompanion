import time
import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from shoppinglist.models import ShoppingList, Item
from shoppinglist.constants import ItemCategory, ItemUnit


@pytest.mark.django_db
def test_shopping_list_and_item_creation():
    # Create a shopping list instance
    shopping_list = ShoppingList.objects.create(name="My Shopping List")

    assert shopping_list.name == "My Shopping List"

    # Create an item and link it to the shopping list
    item = Item.objects.create(
        shopping_list=shopping_list,
        product="Eggs",
        quantity=12,
        category=ItemCategory.DAIRY,
    )

    # Check the attributes of the created item
    assert item.product == "Eggs"
    assert item.quantity == 12
    assert item.category == ItemCategory.DAIRY

    # Check the default value for 'completed' field
    assert item.completed == False

    # Use the related_name to fetch items from the shopping list
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
    # Create a shopping list instance
    shopping_list = ShoppingList.objects.create(name="Deletion Test List")

    # Create multiple items linked to this shopping list
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

    # Assert that there are 3 items linked to the shopping list
    assert Item.objects.filter(shopping_list=shopping_list).count() == 3

    # Store the ID before deletion to use for the check later
    shopping_list_id = shopping_list.id

    # Delete the shopping list
    shopping_list.delete()

    # After deletion, there should be no items linked to the deleted shopping list's ID
    assert Item.objects.filter(shopping_list_id=shopping_list_id).count() == 0


from django.contrib.auth.models import User


@pytest.mark.django_db
def test_user_foreignkey_in_shoppinglist():
    # Test creation of a shopping list with a user
    user = User.objects.create_user(username="testuser", password="testpassword")
    shopping_list_with_user = ShoppingList.objects.create(
        name="List with user", user=user
    )
    assert shopping_list_with_user.user == user

    # Test creation of a shopping list without a user
    shopping_list_without_user = ShoppingList.objects.create(name="List without user")
    assert shopping_list_without_user.user is None

    # Test behavior when a user is deleted
    user_id = user.id
    user.delete()

    # Try to retrieve the shopping list associated with the deleted user
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
    # Create a shopping list instance
    shopping_list = ShoppingList.objects.create(name="Ordering Test List")

    # Create multiple items with varying 'completed' statuses
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

    # Fetch all items and check the ordering
    items = list(Item.objects.all())

    # Assert that the first two items are the ones that are not completed
    assert items[0] == item2  # This item is not completed
    assert items[1] == item1 or items[1] == item3  # These items are completed
    assert items[2] == item1 or items[2] == item3  # These items are completed


@pytest.mark.django_db
def test_enum_choices_in_item():
    # Prepare a shopping list to associate the items with
    shopping_list = ShoppingList.objects.create(name="Test List")

    # Test invalid unit choice
    with pytest.raises(ValidationError):
        item_with_invalid_unit = Item(
            shopping_list=shopping_list,
            product="Invalid Unit Product",
            unit="invalid_unit",
            category=ItemCategory.DAIRY,
        )
        item_with_invalid_unit.full_clean()  # This triggers validation

    # Test invalid category choice
    with pytest.raises(ValidationError):
        item_with_invalid_category = Item(
            shopping_list=shopping_list,
            product="Invalid Category Product",
            unit=ItemUnit.LITER,
            category="invalid_category",
        )
        item_with_invalid_category.full_clean()  # This triggers validation


@pytest.mark.django_db
def test_positive_quantity_in_item():
    # Prepare a shopping list to associate the items with
    shopping_list = ShoppingList.objects.create(name="Test List")

    # Test creating item with negative quantity
    with pytest.raises(ValidationError):
        item_with_negative_quantity = Item(
            shopping_list=shopping_list,
            product="Negative Quantity Product",
            quantity=-1,
            category=ItemCategory.DAIRY,
        )
        item_with_negative_quantity.full_clean()  # This triggers validation

    # Test creating item with zero quantity
    with pytest.raises(ValidationError):
        item_with_zero_quantity = Item(
            shopping_list=shopping_list,
            product="Zero Quantity Product",
            quantity=0,
            category=ItemCategory.DAIRY,
        )
        item_with_zero_quantity.full_clean()  # This triggers validation

    # Create a valid item first
    valid_item = Item.objects.create(
        shopping_list=shopping_list,
        product="Valid Product",
        quantity=10,
        category=ItemCategory.DAIRY,
    )

    # Test updating item to have negative quantity
    valid_item.quantity = -5
    with pytest.raises(ValidationError):
        valid_item.full_clean()  # This triggers validation

    # Test updating item to have zero quantity
    valid_item.quantity = 0
    with pytest.raises(ValidationError):
        valid_item.full_clean()  # This triggers validation


@pytest.mark.django_db
def test_item_additional_notes():
    shopping_list = ShoppingList.objects.create(name="Test List")

    # Create an item with additional notes
    item_note = "This is a note for testing purposes."
    item_with_note = Item.objects.create(
        shopping_list=shopping_list,
        product="Product with Note",
        category=ItemCategory.DAIRY,
        note=item_note,
    )

    # Fetch the item from the database and check its note attribute
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
    # Initial creation of shopping list
    shopping_list = ShoppingList.objects.create(name="My Shopping List")

    # Initial creation of item
    item = Item.objects.create(
        shopping_list=shopping_list,
        product="Eggs",
        quantity=12,
        category=ItemCategory.DAIRY,
    )

    # Record initial timestamps for the item
    initial_created = item.created
    initial_updated = item.updated

    # Ensure a small delay so that the updated timestamp can actually change
    time.sleep(2)

    # Update the item
    item.product = "Updated Eggs"
    item.save()

    # Fetch the updated item from the database
    updated_item = Item.objects.get(pk=item.pk)

    # Assert that created timestamp hasn't changed
    assert initial_created == updated_item.created

    # Assert that updated timestamp has changed
    assert initial_updated < updated_item.updated


@pytest.mark.django_db
def test_text_fields_max_length():
    shopping_list = ShoppingList.objects.create(name="Test List")

    # Test max length for Item product field
    max_length_product = Item._meta.get_field("product").max_length
    assert (
        max_length_product == 200
    )  # replace 200 with the actual max_length you've set if it's different
    with pytest.raises(ValidationError):
        item_with_too_long_product = Item(
            shopping_list=shopping_list,
            product="P" * (max_length_product + 1),
            category=ItemCategory.DAIRY,
        )
        item_with_too_long_product.full_clean()
