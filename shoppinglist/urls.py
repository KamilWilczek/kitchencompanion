from django.urls import path
from .views import (
    ShoppingListView,
    ShoppingListCreateView,
    ShoppingListDetailUpdateView,
    ShoppingListDeleteView,
    ItemUpdateView,
    ItemCreateView,
    ItemDeleteView,
)

app_name = "shoppinglist"

urlpatterns = [
    path("", ShoppingListView.as_view(), name="list"),
    path("create-update/", ShoppingListCreateView.as_view(), name="create"),
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
]
