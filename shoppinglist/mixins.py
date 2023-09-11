from typing import Optional, Any, Dict

from rest_framework import exceptions

from .models import ShoppingList


class ShoppingItemMixin:
    """
    Mixin to centralize the logic of retrieving shopping list from parent_pk.
    """

    kwargs: Dict[str, Any]

    def get_shopping_list(self) -> ShoppingList:
        parent_pk: Optional[str] = self.kwargs.get("parent_pk")
        if parent_pk is None:
            raise exceptions.ValidationError("parent_pk not provided in kwargs.")

        try:
            return ShoppingList.objects.get(pk=parent_pk)
        except ShoppingList.DoesNotExist:
            raise exceptions.NotFound("ShoppingList not found.")
