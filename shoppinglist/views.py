from typing import Union

from decouple import config
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Prefetch, Q, QuerySet
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from .mixins import ShoppingItemMixin
from .models import Item, ShoppingList
from .serializers import ItemSerializer, ShoppingListSerializer


class ShoppingListView(generics.ListAPIView):
    """
    API view to list all the shopping lists along with an annotation of the number of items each list contains.
    """

    serializer_class: type[ShoppingListSerializer] = ShoppingListSerializer

    def get_queryset(self) -> QuerySet[ShoppingList]:
        return ShoppingList.objects.prefetch_related(
            Prefetch("items", queryset=Item.objects.only("id"))
        )


class ShoppingListCreateView(generics.CreateAPIView):
    """
    API view to create a new shopping list.
    """

    serializer_class: type[ShoppingListSerializer] = ShoppingListSerializer


class ShoppingListDetailUpdateView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve or update the details of a specific shopping list.
    """

    serializer_class: type[ShoppingListSerializer] = ShoppingListSerializer

    def get_queryset(self) -> "QuerySet[ShoppingList]":
        user = self.request.user
        return ShoppingList.objects.prefetch_related("items").filter(
            Q(user=user) | Q(shared_with=user)
        )


class ShoppingListDeleteView(generics.DestroyAPIView):
    """
    API view to delete a specific shopping list.
    """

    queryset: QuerySet[ShoppingList] = ShoppingList.objects.all()
    serializer_class: type[ShoppingListSerializer] = ShoppingListSerializer

    def delete(
        self, request: Request, *args: Union[str, int], **kwargs: dict
    ) -> Response:
        instance: ShoppingList = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Shopping list deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class ShoppingListShareView(generics.UpdateAPIView):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer

    def update(self, request, *args, **kwargs):
        shopping_list = self.get_object()
        user_to_share_with_email = request.data.get("email")

        if shopping_list.user != request.user:
            return Response(
                {"detail": "You don't have permission to share this list."},
                status=status.HTTP_403_FORBIDDEN,
            )

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


class ItemCreateView(ShoppingItemMixin, generics.CreateAPIView):
    """
    API view to add a new item to a specific shopping list.
    """

    serializer_class: type[ItemSerializer] = ItemSerializer

    def perform_create(self, serializer: ItemSerializer):
        shopping_list: ShoppingList = self.get_shopping_list()
        serializer.save(shopping_list=shopping_list)


class ItemUpdateView(ShoppingItemMixin, generics.RetrieveUpdateAPIView):
    """
    API view to retrieve or update a specific item within a given shopping list.
    """

    serializer_class: type[ItemSerializer] = ItemSerializer

    def get_queryset(self) -> QuerySet[Item]:
        return Item.objects.filter(shopping_list=self.get_shopping_list())


class ItemDeleteView(ShoppingItemMixin, generics.DestroyAPIView):
    """
    API view to delete a specific item from a given shopping list.
    """

    serializer_class: type[ItemSerializer] = ItemSerializer

    def get_queryset(self) -> QuerySet[Item]:
        return Item.objects.filter(shopping_list=self.get_shopping_list())

    def delete(
        self, request: Request, *args: Union[str, int], **kwargs: dict
    ) -> Response:
        instance: Item = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"detail": "Item deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )
