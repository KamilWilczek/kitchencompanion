from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ItemCreateView, ItemDeleteView, ItemUpdateView, ShoppingListViewSet

router = DefaultRouter()
router.register(r"", ShoppingListViewSet, basename="shoppinglist")

app_name = "shoppinglist"

urlpatterns = [
    path("", include(router.urls)),
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
