from rest_framework import exceptions

from .models import ShoppingList


class ShoppingItemMixin:
    """
    Mixin to centralize the logic of retrieving shopping list from parent_pk.
    """

    def get_shopping_list(self):
        parent_pk = self.kwargs.get("parent_pk")
        try:
            return ShoppingList.objects.get(pk=parent_pk)
        except ShoppingList.DoesNotExist:
            raise exceptions.NotFound("ShoppingList not found.")
