from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from .constants import ItemCategory, ItemUnit


class ShoppingList(models.Model):
    """
    Represents a shopping list created by a user.

    Attributes:
    - user: The user who created the shopping list.
    - name: The name of the shopping list.
    - description: A brief description or notes for the shopping list.
    - created: Timestamp when the shopping list was created.
    - updated: Timestamp when the shopping list was last updated.
    - completed: Flag to mark if the shopping list is completed.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["created"]
        verbose_name = "shopping list"
        verbose_name_plural = "shopping lists"


class Item(models.Model):
    """
    Represents an item in a shopping list.

    Attributes:
    - shopping_list: The shopping list to which the item belongs.
    - product: Name of the product.
    - quantity: Quantity of the product required.
    - unit: The unit of measurement for the quantity (e.g., kg, pcs).
    - category: The category the product falls under (e.g., dairy, fruits).
    - note: Additional notes or description for the item.
    - created: Timestamp when the item was added to the list.
    - updated: Timestamp when the item details were last updated.
    - completed: Flag to mark if the item has been purchased/completed.
    """

    shopping_list = models.ForeignKey(
        ShoppingList, on_delete=models.CASCADE, related_name="item"
    )
    product = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(
        null=True, blank=True, validators=[MinValueValidator(1)]
    )
    unit = models.CharField(
        max_length=20, choices=ItemUnit.choices, null=True, blank=True
    )
    category = models.CharField(max_length=25, choices=ItemCategory.choices)
    note = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False, db_index=True)

    def __str__(self) -> str:
        return self.product

    class Meta:
        ordering = ["completed"]
        verbose_name = "item"
        verbose_name_plural = "items"
