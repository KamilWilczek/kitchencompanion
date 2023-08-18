from django.contrib import admin

from .models import Item, ShoppingList


class ItemInline(admin.StackedInline):
    model = Item
    extra = 0


class ShoppingListAdmin(admin.ModelAdmin):
    inlines = [ItemInline]
    readonly_fields = ["created", "updated"]


admin.site.register(ShoppingList, ShoppingListAdmin)
