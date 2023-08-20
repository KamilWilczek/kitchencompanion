from rest_framework import serializers
from .models import ShoppingList, Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "product", "quantity", "unit", "note", "category", "completed")


class ShoppingListSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    items_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ShoppingList
        fields = "__all__"
