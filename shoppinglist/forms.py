from django import forms

from .models import Item, ShoppingList


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"

    # def __init__(self, *args, **kwargs):


class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = "__all__"

    # def __init__(self, *args, **kwargs):
