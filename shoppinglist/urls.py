from django.urls import path

from .views import (
    ItemCreateView,
    ItemDeleteView,
    ItemUpdateView,
    ShoppingListCreateView,
    ShoppingListDeleteView,
    ShoppingListDetailUpdateView,
    ShoppingListShareView,
    ShoppingListView,
)

app_name = "shoppinglist"

urlpatterns = [
    path("", ShoppingListView.as_view(), name="list"),
    path("create/", ShoppingListCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", ShoppingListDetailUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", ShoppingListDeleteView.as_view(), name="delete"),
    path("<int:parent_pk>/item/", ItemCreateView.as_view(), name="item-create"),
    path(
        "<int:parent_pk>/item/<int:pk>/", ItemUpdateView.as_view(), name="item-update"
    ),
    path(
        "<int:parent_pk>/item/<int:pk>/delete/",
        ItemDeleteView.as_view(),
        name="item-delete",
    ),
    path(
        "share-shopping-list/<int:pk>/",
        ShoppingListShareView.as_view(),
        name="share_shopping_list",
    ),
]
