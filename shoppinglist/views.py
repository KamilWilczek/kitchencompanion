from django.db.models import Count
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import ShoppingListSerializer, ItemSerializer

from .models import Item, ShoppingList


def error_response(detail, status_code):
    return Response({"detail": detail}, status=status_code)


class ShoppingListView(generics.ListAPIView):
    queryset = ShoppingList.objects.annotate(items_count=Count("items"))
    serializer_class = ShoppingListSerializer


class ShoppingListCreateView(generics.CreateAPIView):
    serializer_class = ShoppingListSerializer


class ShoppingListDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = ShoppingList.objects.prefetch_related("items")
    serializer_class = ShoppingListSerializer


class ShoppingListDeleteView(generics.DestroyAPIView):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )


class ItemUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        parent_pk = self.kwargs["parent_pk"]
        return Item.objects.filter(shoppinglist__pk=parent_pk)


class ItemCreateView(generics.CreateAPIView):
    serializer_class = ItemSerializer

    def perform_create(self, serializer):
        parent_pk = self.kwargs.get("parent_pk")
        try:
            shopping_list = ShoppingList.objects.get(pk=parent_pk)
            serializer.save(shoppinglist=shopping_list)
        except ShoppingList.DoesNotExist:
            raise error_response("ShoppingList not found.", status.HTTP_404_NOT_FOUND)


class ItemDeleteView(generics.DestroyAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        parent_pk = self.kwargs["parent_pk"]
        return Item.objects.filter(shoppinglist__pk=parent_pk)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Item deleted successfully."}, status=status.HTTP_200_OK
        )
