from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import ShoppingListSerializer, ItemSerializer

from .models import Item, ShoppingList


# # List of shopping lists
@api_view(["GET"])
def shoppinglist_list_view(request):
    qs = ShoppingList.objects.annotate(items_count=Count("items"))
    serialized_qs = ShoppingListSerializer(qs, many=True)
    return Response(serialized_qs.data, status=status.HTTP_200_OK)


# Creating shopping list
@api_view(["POST"])
def shoppinglist_create_view(request):
    if request.method == "POST":
        serializer = ShoppingListSerializer(data=request.data)

        if serializer.is_valid():
            obj = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Editing of shopping list
@api_view(["GET", "PUT"])
def shoppinglist_update_view(request, id=None):
    obj = get_object_or_404(ShoppingList.objects.prefetch_related("items"), id=id)

    # For GET request, return the current state of the ShoppingList
    if request.method == "GET":
        serializer = ShoppingListSerializer(obj)
        return Response(serializer.data)

    # For PUT request, update the ShoppingList
    if request.method == "PUT":
        serializer = ShoppingListSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Deleting shopping lists
@api_view(["DELETE"])
def shoppinglist_delete_view(request, id=None):
    try:
        obj = ShoppingList.objects.get(id=id)
    except ShoppingList.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        obj.delete()
        return Response(
            {"detail": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )


# Edit item
@api_view(["GET", "PUT"])
def item_update_view(request, parent_id=None, id=None):
    item = get_object_or_404(Item, shoppinglist__id=parent_id, id=id)

    # For GET request, return the current state of the Item
    if request.method == "GET":
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    # For PUT request, update the Item
    elif request.method == "PUT":
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Creating item
@api_view(["POST"])
def item_create_view(request, parent_id=None):
    try:
        parent_obj = ShoppingList.objects.get(id=parent_id)
    except ShoppingList.DoesNotExist:
        return Response(
            {"detail": "ShoppingList not found."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(shoppinglist=parent_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Deleting item
@api_view(["DELETE"])
def item_delete_view(request, parent_id=None, id=None):
    try:
        # Fetch the specific ShoppingList based on parent_id
        shopping_list = ShoppingList.objects.get(id=parent_id)

        # Try to get the item within that shopping list with the provided id
        item = shopping_list.items.get(
            id=id
        )  # Assuming "items" is the related name for the Item model
        item.delete()

        return Response(
            {"detail": "Item deleted successfully."}, status=status.HTTP_200_OK
        )

    except ShoppingList.DoesNotExist:
        return Response(
            {"detail": "Shopping List not found."}, status=status.HTTP_404_NOT_FOUND
        )
    except Item.DoesNotExist:
        return Response({"detail": "Item not found."}, status=status.HTTP_404_NOT_FOUND)
