from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import ShoppingListSerializer

from .models import Item, ShoppingList


from .forms import ItemForm, ShoppingListForm


# # List of shopping lists
@api_view(["GET"])
def shoppinglist_list_view(request):
    qs = ShoppingList.objects.annotate(items_count=Count("item"))
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
    obj = get_object_or_404(ShoppingList, id=id)

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
def item_update_view(request, parent_id=None, id=None):
    parent_obj = ShoppingList.objects.get(id=parent_id, user=request.user)
    instance = Item.objects.get(shoppinglist=parent_obj, id=id)
    form = ItemForm(request.POST or None, instance=instance)
    return_from_edit = reverse("shoppinglist:update", kwargs={"id": parent_obj.id})
    context = {
        "return_from_edit": return_from_edit,
        "form": form,
        "object": instance,
        "id": parent_obj.id,
        "parent_id": parent_obj.id,
    }
    if form.is_valid():
        new_obj = form.save()
        new_obj.save()
        context["object"] = new_obj
        return render(request, "shoppinglist/partials/item-form.html", context)
    return render(request, "shoppinglist/partials/item-form.html", context)


# Creating item
def item_create_view(request, parent_id=None):
    parent_obj = ShoppingList.objects.get(id=parent_id, user=request.user)
    print(parent_obj)
    form = ItemForm(request.POST or None)
    return_from_create = reverse(
        "shoppinglist:item-create", kwargs={"parent_id": parent_obj.id}
    )
    context = {
        "return_from_create": return_from_create,
        "form": form,
        "parent_id": parent_obj.id,
    }
    if form.is_valid():
        obj = form.save()
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, "shoppinglist/partials/item-form.html", context)
