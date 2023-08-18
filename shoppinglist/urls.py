from django.urls import path

from .views import (
    shoppinglist_list_view,
    shoppinglist_create_view,
    shoppinglist_update_view,
    shoppinglist_delete_view,
    item_update_view,
    item_create_view,
)

app_name = "shoppinglist"

urlpatterns = [
    path("", shoppinglist_list_view, name="list"),
    path("create-update/", shoppinglist_create_view, name="create"),
    path("<int:id>/edit/", shoppinglist_update_view, name="update"),
    path("<int:id>/delete/", shoppinglist_delete_view, name="delete"),
    path(
        "<int:parent_id>/item/",
        item_create_view,
        name="item-create",
    ),
    path(
        "<int:parent_id>/item/<int:id>/",
        item_update_view,
        name="item-update",
    ),
]
