from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ShoppingListSerializer

from .models import Item, ShoppingList


from .forms import ItemForm, ShoppingListForm


# # List of shopping lists
# def shoppinglist_list_view(request):
#     qs = ShoppingList.objects.all
#     context = {"shoppinglists": qs}
#     return render(request, "shoppinglist/list.html", context)
@api_view(["GET"])
def shoppinglist_list_view(request):
    qs = ShoppingList.objects.all()
    serialized_qs = ShoppingListSerializer(qs, many=True)
    return Response(serialized_qs.data)


# Creating shopping list
def shoppinglist_create_view(request):
    form = ShoppingListForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        obj = form.save()
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, "shoppinglist/create-update.html", context)


# Editing of shopping list
def shoppinglist_update_view(request, id=None):
    obj = get_object_or_404(ShoppingList, id=id)
    form = ShoppingListForm(request.POST or None, instance=obj)
    url = reverse("shoppinglist:item-create", kwargs={"parent_id": obj.id})
    context = {
        "form": form,
        "object": obj,
        "parent_id": obj.id,
        "url": url,
    }
    if form.is_valid():
        form.save()
        context["message"] = "Data saved"
    return render(request, "shoppinglist/create-update.html", context)


# Deleting shopping lists
def shoppinglist_delete_view(request, id=None):
    obj = ShoppingList.objects.get(id=id, user=request.user)
    if request.method == "POST":
        obj.delete()
        success_url = reverse("shoppinglist:list")
        return redirect(success_url)
    context = {"object": obj}
    return render(request, "shoppinglist/delete.html", context)


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
