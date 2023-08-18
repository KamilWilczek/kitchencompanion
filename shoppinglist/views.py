from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404

from .models import Item, ShoppingList


from .forms import ItemForm, ShoppingListForm


# List of shopping lists
def shopping_list_list_view(request):
    qs = ShoppingList.objects.all
    context = {"shopping_lists": qs}
    return render(request, "shopping_list/list.html", context)


# Creating shopping list
def shopping_list_create_view(request):
    form = ShoppingListForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        obj = form.save()
        obj.save()
        return redirect(obj.get_absolute_url())
    return render(request, "shopping_list/create-update.html", context)


# Editing of shopping list
def shopping_list_update_view(request, id=None):
    obj = get_object_or_404(ShoppingList, id=id)
    form = ShoppingListForm(request.POST or None, instance=obj)
    url = reverse("shopping_list:item-create", kwargs={"parent_id": obj.id})
    context = {
        "form": form,
        "object": obj,
        "parent_id": obj.id,
        "url": url,
    }
    if form.is_valid():
        form.save()
        context["message"] = "Data saved"
    return render(request, "shopping_list/create-update.html", context)


# Deleting shopping lists
def shopping_list_delete_view(request, id=None):
    obj = ShoppingList.objects.get(id=id, user=request.user)
    if request.method == "POST":
        obj.delete()
        success_url = reverse("shopping_list:list")
        return redirect(success_url)
    context = {"object": obj}
    return render(request, "shopping_list/delete.html", context)


# Edit item
def item_update_view(request, parent_id=None, id=None):
    parent_obj = ShoppingList.objects.get(id=parent_id, user=request.user)
    instance = Item.objects.get(shopping_list=parent_obj, id=id)
    form = ItemForm(request.POST or None, instance=instance)
    return_from_edit = reverse("shopping_list:update", kwargs={"id": parent_obj.id})
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
        return render(request, "shopping_list/partials/item-form.html", context)
    return render(request, "shopping_list/partials/item-form.html", context)


# Creating item
def item_create_view(request, parent_id=None):
    parent_obj = ShoppingList.objects.get(id=parent_id, user=request.user)
    print(parent_obj)
    form = ItemForm(request.POST or None)
    return_from_create = reverse(
        "shopping_list:item-create", kwargs={"parent_id": parent_obj.id}
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
    return render(request, "shopping_list/partials/item-form.html", context)
