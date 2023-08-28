from django.db.models import Count
from rest_framework.response import Response
from rest_framework import generics, status

from .models import Item, ShoppingList
from .mixins import ShoppingItemMixin
from .serializers import ShoppingListSerializer, ItemSerializer


class ShoppingListView(generics.ListAPIView):
    """
    API view to list all the shopping lists along with an annotation of the number of items each list contains.
    """

    queryset = ShoppingList.objects.annotate(items_count=Count("item"))
    serializer_class = ShoppingListSerializer


class ShoppingListCreateView(generics.CreateAPIView):
    """
    API view to create a new shopping list.
    """

    serializer_class = ShoppingListSerializer


class ShoppingListDetailUpdateView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve or update the details of a specific shopping list.
    """

    queryset = ShoppingList.objects.prefetch_related("item")
    serializer_class = ShoppingListSerializer


class ShoppingListDeleteView(generics.DestroyAPIView):
    """
    API view to delete a specific shopping list.
    """

    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer

    def delete(self, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Shopping list deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ItemUpdateView(ShoppingItemMixin, generics.RetrieveUpdateAPIView):
    """
    API view to retrieve or update a specific item within a given shopping list.
    """

    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.filter(shoppinglist=self.get_shopping_list())


class ItemCreateView(ShoppingItemMixin, generics.CreateAPIView):
    """
    API view to add a new item to a specific shopping list.
    """

    serializer_class = ItemSerializer

    def perform_create(self, serializer):
        shopping_list = self.get_shopping_list()
        serializer.save(shoppinglist=shopping_list)


class ItemDeleteView(ShoppingItemMixin, generics.DestroyAPIView):
    """
    API view to delete a specific item from a given shopping list.
    """

    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.filter(shoppinglist=self.get_shopping_list())

    def delete(self, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Item deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )
