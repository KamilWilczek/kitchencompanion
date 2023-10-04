import pytest
from rest_framework import exceptions

from shoppinglist.mixins import ShoppingItemMixin
from shoppinglist.models import ShoppingList


class TestShoppingItemMixin:
    @pytest.mark.django_db
    def test_get_shopping_list_retrieves_correct_shopping_list(
        self, shopping_list: ShoppingList
    ) -> None:
        mixin_instance = ShoppingItemMixin()
        mixin_instance.kwargs = {"shoppinglist_pk": shopping_list.pk}
        retrieved_shopping_list = mixin_instance.get_shopping_list()

        assert retrieved_shopping_list == shopping_list

    def test_get_shopping_list_raises_validation_error_when_shoppinglist_pk_not_provided(
        self,
    ) -> None:
        mixin_instance = ShoppingItemMixin()
        mixin_instance.kwargs = {}

        with pytest.raises(exceptions.ValidationError):
            mixin_instance.get_shopping_list()

    @pytest.mark.django_db
    def test_get_shopping_list_raises_not_found_when_shopping_list_does_not_exist(
        self,
    ) -> None:
        mixin_instance = ShoppingItemMixin()
        non_existent_shopping_list_pk = 1
        mixin_instance.kwargs = {"shoppinglist_pk": non_existent_shopping_list_pk}

        with pytest.raises(exceptions.NotFound):
            mixin_instance.get_shopping_list()
