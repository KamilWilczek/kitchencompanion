import pytest
from shoppinglist.models import ShoppingList, Item


@pytest.mark.django_db
def test_shopping_list_and_item_creation():
    # Create a shopping list instance
    shopping_list = ShoppingList.objects.create(name="My Shopping List")
    assert shopping_list.name == "My Shopping List"

    # Create an item and link it to the shopping list
    item = Item.objects.create(
        shopping_list=shopping_list, product="Eggs", quantity=12, category="DIARY"
    )

    # Check the attributes of the created item
    assert item.product == "Eggs"
    assert item.quantity == 12
    assert item.category == "DIARY"

    # Use the related_name to fetch items from the shopping list
    items_linked_to_list = shopping_list.item.all()
    assert len(items_linked_to_list) == 1
    assert items_linked_to_list[0].product == "Eggs"
