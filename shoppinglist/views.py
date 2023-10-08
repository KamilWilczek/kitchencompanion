from decouple import config
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Q, QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .mixins import ShoppingItemMixin
from .models import Item, ShoppingList
from .permissions import IsOwnerOrSharedUser
from .serializers import ItemSerializer, ShoppingListSerializer


class ShoppingListViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrSharedUser]
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer

    def get_queryset(self) -> QuerySet[ShoppingList]:
        user = self.request.user
        if user.is_authenticated:
            return ShoppingList.objects.prefetch_related("items").filter(
                Q(user=user) | Q(shared_with=user)
            )
        return ShoppingList.objects.none()

    @action(detail=True, methods=["put"])
    def share(self, request, pk: int | None = None):
        shopping_list = self.get_object()
        user_to_share_with_email = request.data.get("email")

        if user_to_share_with_email == request.user.email:
            return Response(
                {"detail": "You cannot share the list with yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_to_share_with = get_user_model().objects.get(
                email=user_to_share_with_email
            )
        except get_user_model().DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_400_BAD_REQUEST
            )

        if shopping_list.shared_with.filter(email=user_to_share_with_email).exists():
            return Response(
                {
                    "detail": f"Shopping list was already shared with {user_to_share_with_email}."
                },
                status=status.HTTP_200_OK,
            )

        shopping_list.shared_with.add(user_to_share_with)
        shopping_list.save()

        subject = "Shopping List Shared With You"
        message = f"{request.user.email} has shared a shopping list with you."
        from_email = config("EMAIL_HOST_USER")
        to_email = [user_to_share_with_email]

        send_mail(subject, message, from_email, to_email, fail_silently=False)

        return Response({"detail": "Shopping list shared successfully."})

    @action(detail=True, methods=["patch"], url_path="unshare/(?P<user_pk>[^/.]+)")
    def unshare(self, request: Request, pk: int | None = None, **kwargs: str | int):
        shopping_list = self.get_object()
        user_id_to_unshare = kwargs.get("user_pk")

        if user_id_to_unshare is None:
            return Response(
                {"detail": "Invalid user ID."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_to_unshare = get_user_model().objects.get(pk=user_id_to_unshare)
        except get_user_model().DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_400_BAD_REQUEST
            )

        if user_to_unshare not in shopping_list.shared_with.all():
            return Response(
                {"detail": "This list is not shared with the specified user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        shopping_list.shared_with.remove(user_to_unshare)
        return Response({"detail": "Successfully unshared the shopping list."})

    def destroy(self, request: Request, *args: str | int, **kwargs: dict) -> Response:
        shopping_list: ShoppingList = self.get_object()

        if shopping_list.user == request.user:
            return super().destroy(request, *args, **kwargs)

        if request.user in shopping_list.shared_with.all():
            shopping_list.shared_with.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {"detail": "You don't have permission to delete this list."},
            status=status.HTTP_403_FORBIDDEN,
        )


class ItemViewSet(ShoppingItemMixin, ModelViewSet):
    """
    API viewset for CRUD operations on a shopping list item.
    """

    queryset = Item.objects.all()
    serializer_class: type[ItemSerializer] = ItemSerializer

    def get_queryset(self) -> QuerySet[Item]:
        return Item.objects.filter(shopping_list=self.get_shopping_list())

    def perform_create(self, serializer: ItemSerializer):
        shopping_list: ShoppingList = self.get_shopping_list()
        serializer.save(shopping_list=shopping_list)

    def destroy(self, request: Request, *args: str | int, **kwargs: dict):
        instance: Item = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Item deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )
