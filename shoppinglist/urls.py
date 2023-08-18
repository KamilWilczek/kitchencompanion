from django.urls import path

from .views import (
    shopping_list_list_view,
    shopping_list_create_view,
    shopping_list_update_view,
    shopping_list_delete_view,
    item_update_view,
    item_create_view,
)

app_name = "shopping_list"

urlpatterns = [
    path("", shopping_list_list_view, name="list"),
    path("create-update/", shopping_list_create_view, name="create"),
    path("<int:id>/edit/", shopping_list_update_view, name="update"),
    path("<int:id>/delete/", shopping_list_delete_view, name="delete"),
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
