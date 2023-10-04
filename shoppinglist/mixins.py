from typing import Any, Dict, Optional

from rest_framework import exceptions

from .models import ShoppingList


class ShoppingItemMixin:
    """
    Mixin to centralize the logic of retrieving shopping list from shopping_list_pk.
    """

    kwargs: Dict[str, Any]

    def get_shopping_list(self) -> ShoppingList:
        shopping_list_pk: Optional[str] = self.kwargs.get("shoppinglist_pk")
        if shopping_list_pk is None:
            raise exceptions.ValidationError("shopping_list_pk not provided in kwargs.")

        try:
            return ShoppingList.objects.get(pk=shopping_list_pk)
        except ShoppingList.DoesNotExist:
            raise exceptions.NotFound("ShoppingList not found.")
