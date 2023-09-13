from typing import Type

from rest_framework import serializers

from .models import Item, ShoppingList


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model: Type[Item] = Item
        fields = ("id", "product", "quantity", "unit", "note", "category", "completed")


class ShoppingListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model: Type[ShoppingList] = ShoppingList
        fields = "__all__"

    def get_items_count(self, obj: ShoppingList) -> int:
        try:
            return obj.items.count()
        except AttributeError:
            return 0
