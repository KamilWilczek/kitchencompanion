from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import ItemViewSet, ShoppingListViewSet

router = DefaultRouter()
router.register(r"", ShoppingListViewSet, basename="shoppinglist")

shopping_list_router = routers.NestedSimpleRouter(router, r"", lookup="shoppinglist")
shopping_list_router.register(r"item", ItemViewSet, basename="shoppinglist-item")

app_name = "shoppinglist"

urlpatterns = [
    path("", include(router.urls)),
    path("", include(shopping_list_router.urls)),
]
