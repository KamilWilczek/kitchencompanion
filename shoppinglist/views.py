from typing import List, Union
from django.db.models import Count, QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, status

from .models import Item, ShoppingList
from .mixins import ShoppingItemMixin
from .serializers import ShoppingListSerializer, ItemSerializer


class ShoppingListView(generics.ListAPIView):
    """
    API view to list all the shopping lists along with an annotation of the number of items each list contains.
    """

    queryset: QuerySet[ShoppingList] = ShoppingList.objects.annotate(
        items_count=Count("item")
    )
    serializer_class: type[ShoppingListSerializer] = ShoppingListSerializer


class ShoppingListCreateView(generics.CreateAPIView):
    """
    API view to create a new shopping list.
    """

    serializer_class: type[ShoppingListSerializer] = ShoppingListSerializer


class ShoppingListDetailUpdateView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve or update the details of a specific shopping list.
    """

    queryset: QuerySet[ShoppingList] = ShoppingList.objects.prefetch_related("item")
    serializer_class: type[ShoppingListSerializer] = ShoppingListSerializer


class ShoppingListDeleteView(generics.DestroyAPIView):
    """
    API view to delete a specific shopping list.
    """

    queryset: QuerySet[ShoppingList] = ShoppingList.objects.all()
    serializer_class: type[ShoppingListSerializer] = ShoppingListSerializer

    def delete(
        self, request: Request, *args: Union[str, int], **kwargs: dict
    ) -> Response:
        instance: ShoppingList = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Shopping list deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ItemCreateView(ShoppingItemMixin, generics.CreateAPIView):
    """
    API view to add a new item to a specific shopping list.
    """

    serializer_class: type[ItemSerializer] = ItemSerializer

    def perform_create(self, serializer: ItemSerializer):
        shopping_list: ShoppingList = self.get_shopping_list()
        serializer.save(shopping_list=shopping_list)


class ItemUpdateView(ShoppingItemMixin, generics.RetrieveUpdateAPIView):
    """
    API view to retrieve or update a specific item within a given shopping list.
    """

    serializer_class: type[ItemSerializer] = ItemSerializer

    def get_queryset(self) -> QuerySet[Item]:
        return Item.objects.filter(shopping_list=self.get_shopping_list())


class ItemDeleteView(ShoppingItemMixin, generics.DestroyAPIView):
    """
    API view to delete a specific item from a given shopping list.
    """

    serializer_class: type[ItemSerializer] = ItemSerializer

    def get_queryset(self) -> QuerySet[Item]:
        return Item.objects.filter(shopping_list=self.get_shopping_list())

    def delete(
        self, request: Request, *args: Union[str, int], **kwargs: dict
    ) -> Response:
        instance: Item = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Item deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )
