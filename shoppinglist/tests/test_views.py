from typing import Dict, List

import pytest
from django.db import connections
from django.test.utils import CaptureQueriesContext
from rest_framework import status
from rest_framework.test import APIClient

from conftest import create_item, create_multiple_items, create_shopping_list
from shoppinglist.constants import ItemCategory, ItemUnit
from shoppinglist.models import ShoppingList
from users.models import CustomUser

from .error_messages import ERRORS
from .urls import URLS


@pytest.mark.django_db
class TestShoppingListViewSet:
    def test_all_shopping_lists_are_returned(
        self, authenticated_user: CustomUser, authenticated_api_client: APIClient
    ) -> None:
        create_shopping_list(name="Shopping List 1", user=authenticated_user)
        create_shopping_list(name="Shopping List 2", user=authenticated_user)
        create_shopping_list(name="Shopping List 3", user=authenticated_user)

        response = authenticated_api_client.get(f"{URLS.SHOPPING_LIST_URL}/")

        assert response.status_code == status.HTTP_200_OK, response.content
        assert len(response.data) == 3

    def test_items_count_returns_correct_number(
        self, authenticated_user: CustomUser, authenticated_api_client: APIClient
    ) -> None:
        shopping_list_1 = create_shopping_list(
            name="Shopping List 1", user=authenticated_user
        )
        shopping_list_2 = create_shopping_list(
            name="Shopping List 2", user=authenticated_user
        )
        items_data_1: List[Dict[str, str | ItemCategory]] = [
            {"product": "Milk", "category": ItemCategory.DAIRY},
            {"product": "Bread", "category": ItemCategory.BREAD},
            {"product": "Apples", "category": ItemCategory.FRUITS_VEGETABLES},
        ]
        items_data_2: List[Dict[str, str | ItemCategory]] = [
            {"product": "Beef", "category": ItemCategory.MEAT},
            {"product": "Butter", "category": ItemCategory.FATS},
        ]

        create_multiple_items(shopping_list_1, items_data_1)
        create_multiple_items(shopping_list_2, items_data_2)

        response = authenticated_api_client.get(f"{URLS.SHOPPING_LIST_URL}/")

        assert response.status_code == status.HTTP_200_OK, response.content
        assert response.data[0]["items_count"] == 3
        assert response.data[1]["items_count"] == 2

    def test_items_count_with_no_items(
        self, authenticated_user: CustomUser, authenticated_api_client: APIClient
    ) -> None:
        create_shopping_list(name="Empty Shopping List", user=authenticated_user)

        response = authenticated_api_client.get(f"{URLS.SHOPPING_LIST_URL}/")

        assert response.status_code == status.HTTP_200_OK, response.content
        assert response.data[0]["items_count"] == 0

    def test_database_queries_optimization(
        self, authenticated_user: CustomUser, authenticated_api_client: APIClient
    ) -> None:
        shopping_list_1 = create_shopping_list(
            name="Shopping List 1", user=authenticated_user
        )
        shopping_list_2 = create_shopping_list(
            name="Shopping List 2", user=authenticated_user
        )

        items_data_1: List[Dict[str, str | ItemCategory]] = [
            {"product": "Milk", "category": ItemCategory.DAIRY},
            {"product": "Bread", "category": ItemCategory.BREAD},
            {"product": "Apples", "category": ItemCategory.FRUITS_VEGETABLES},
        ]

        items_data_2: List[Dict[str, str | ItemCategory]] = [
            {"product": "Beef", "category": ItemCategory.MEAT},
            {"product": "Butter", "category": ItemCategory.FATS},
        ]

        create_multiple_items(shopping_list_1, items_data_1)
        create_multiple_items(shopping_list_2, items_data_2)

        with CaptureQueriesContext(connections["default"]) as context:
            response = authenticated_api_client.get(f"{URLS.SHOPPING_LIST_URL}/")
            assert response.status_code == status.HTTP_200_OK, response.content

            EXPECTED_NUMBER_OF_QUERIES = 5
            assert (
                len(context) == EXPECTED_NUMBER_OF_QUERIES
            ), f"Expected {EXPECTED_NUMBER_OF_QUERIES} queries, but got {len(context)} queries"

    def test_create_shopping_list(
        self, authenticated_user: CustomUser, authenticated_api_client: APIClient
    ) -> None:
        data: Dict[str, int | str] = {
            "user": authenticated_user.id,
            "name": "Shopping List",
        }

        response = authenticated_api_client.post(
            f"{URLS.SHOPPING_LIST_URL}/", data=data
        )

        assert response.status_code == status.HTTP_201_CREATED, response.content
        assert response.data["name"] == data["name"]
        assert ShoppingList.objects.filter(name=data["name"]).exists()

    def test_create_shopping_list_missing_required_fields(
        self, authenticated_user: CustomUser, authenticated_api_client: APIClient
    ) -> None:
        data: Dict[str, int | str] = {
            "user": authenticated_user.id,
            "description": "Groceries",
        }

        response = authenticated_api_client.post(
            f"{URLS.SHOPPING_LIST_URL}/", data=data
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
        assert response.data == {"name": ERRORS.FIELD_REQUIRED_ERROR}

    @pytest.mark.parametrize(
        "invalid_data, expected_response",
        [
            (
                {
                    "user": "invalid_user_id",
                    "name": "",
                    "description": 67890,
                    "completed": "true_string",
                },
                {
                    "user": [ERRORS.INCORRECT_TYPE_ERROR],
                    "name": [ERRORS.NOT_BLANK_ERROR],
                    "completed": [ERRORS.INVALID_BOOLEAN_ERROR],
                },
            ),
        ],
    )
    def test_create_shopping_list_with_invalid_data_types(
        self,
        authenticated_api_client: APIClient,
        invalid_data: Dict[str, str | int],
        expected_response: Dict[str, List[str]],
    ) -> None:
        response = authenticated_api_client.post(
            f"{URLS.SHOPPING_LIST_URL}/", data=invalid_data
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
        assert response.data == expected_response

    def test_create_unique_shopping_list_multiple_times(
        self, authenticated_user: CustomUser, authenticated_api_client: APIClient
    ) -> None:
        data: Dict[str, int | str] = {
            "user": authenticated_user.id,
            "name": "Shopping List",
        }

        response1 = authenticated_api_client.post(
            f"{URLS.SHOPPING_LIST_URL}/", data=data
        )
        assert response1.status_code == status.HTTP_201_CREATED, response1.content

        response2 = authenticated_api_client.post(
            f"{URLS.SHOPPING_LIST_URL}/", data=data
        )
        assert response2.status_code == status.HTTP_201_CREATED, response2.content

        assert response1.data["id"] != response2.data["id"]

    def test_retrieve_shopping_list_by_pk(
        self, authenticated_api_client: APIClient, shopping_list: ShoppingList
    ) -> None:
        url = URLS.SHOPPING_LIST_DETAIL_URL.format(pk=shopping_list.pk)
        response = authenticated_api_client.get(url)

        assert response.status_code == status.HTTP_200_OK, response.content
        assert response.data["name"] == shopping_list.name

    def test_retrieve_someone_elses_shopping_list(
        self, authenticated_api_client: APIClient, external_user: CustomUser
    ) -> None:
        shopping_list_owned_by_another_user = create_shopping_list(user=external_user)

        url = URLS.SHOPPING_LIST_DETAIL_URL.format(
            pk=shopping_list_owned_by_another_user.pk
        )

        response = authenticated_api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content
        assert response.data == ERRORS.NOT_FOUND_ERROR

    def test_retrieve_shared_shopping_list(
        self,
        authenticated_api_client: APIClient,
        authenticated_user: CustomUser,
        external_user: CustomUser,
    ) -> None:
        shopping_list_owned_by_another_user = create_shopping_list(user=external_user)
        shopping_list_owned_by_another_user.shared_with.add(authenticated_user)

        url = URLS.SHOPPING_LIST_DETAIL_URL.format(
            pk=shopping_list_owned_by_another_user.pk
        )

        response = authenticated_api_client.get(url)

        assert response.status_code == status.HTTP_200_OK, response.content
        assert shopping_list_owned_by_another_user.name == "Test List"

    def test_update_shopping_list_by_pk(
        self, authenticated_api_client: APIClient, shopping_list: ShoppingList
    ) -> None:
        url = URLS.SHOPPING_LIST_DETAIL_URL.format(pk=shopping_list.pk)
        data: Dict[str, str] = {
            "name": "Test List",
        }

        response = authenticated_api_client.put(url, data=data)

        assert response.status_code == status.HTTP_200_OK, response.content
        assert response.data["name"] == data["name"]

    def test_update_someone_elses_shopping_list(
        self, authenticated_api_client: APIClient, external_user: CustomUser
    ) -> None:
        shopping_list_owned_by_another_user = create_shopping_list(user=external_user)
        data: Dict[str, str] = {
            "name": "Test List",
        }

        url = URLS.SHOPPING_LIST_DETAIL_URL.format(
            pk=shopping_list_owned_by_another_user.pk
        )

        response = authenticated_api_client.put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content
        assert response.data == ERRORS.NOT_FOUND_ERROR

    def test_update_shared_shopping_list(
        self,
        authenticated_api_client: APIClient,
        authenticated_user: CustomUser,
        external_user: CustomUser,
    ) -> None:
        shopping_list_owned_by_another_user = create_shopping_list(user=external_user)
        shopping_list_owned_by_another_user.shared_with.add(authenticated_user)
        data: Dict[str, str] = {
            "name": "Test List",
        }

        url = URLS.SHOPPING_LIST_DETAIL_URL.format(
            pk=shopping_list_owned_by_another_user.pk
        )

        response = authenticated_api_client.put(url, data=data)

        assert response.status_code == status.HTTP_200_OK, response.content
        assert shopping_list_owned_by_another_user.name == "Test List"

    @pytest.mark.parametrize(
        "invalid_data, expected_response",
        [
            (
                {
                    "user": "invalid_user_id",
                    "name": 12345,
                    "description": 67890,
                    "completed": "true_string",
                },
                {
                    "user": [ERRORS.INCORRECT_TYPE_ERROR],
                    "completed": [ERRORS.INVALID_BOOLEAN_ERROR],
                },
            ),
        ],
    )
    def test_update_shopping_list_with_invalid_data(
        self,
        authenticated_api_client: APIClient,
        shopping_list: ShoppingList,
        invalid_data: Dict[str, str | int],
        expected_response: Dict[str, List[str]],
    ) -> None:
        url = URLS.SHOPPING_LIST_DETAIL_URL.format(pk=shopping_list.pk)
        response = authenticated_api_client.put(url, data=invalid_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
        assert response.data == expected_response

    def test_retrieve_non_existent_shopping_list(
        self, authenticated_api_client: APIClient
    ):
        non_existent_shopping_list_pk = 1
        url = URLS.SHOPPING_LIST_DETAIL_URL.format(pk=non_existent_shopping_list_pk)
        response = authenticated_api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content
        assert response.data == ERRORS.NOT_FOUND_ERROR

    def test_share_shopping_list(
        self,
        authenticated_api_client: APIClient,
        shopping_list: ShoppingList,
        external_user: CustomUser,
    ) -> None:
        email_shared_with = external_user.email
        data = {"email": email_shared_with}
        url = URLS.SHOPPING_LIST_SHARE_URL.format(pk=shopping_list.pk)
        response = authenticated_api_client.put(url, data=data)

        assert response.status_code == status.HTTP_200_OK, response.content
        assert response.data == {"detail": "Shopping list shared successfully."}

    def test_share_shopping_list_user_not_exist(
        self,
        authenticated_api_client: APIClient,
        shopping_list: ShoppingList,
    ) -> None:
        email_shared_with = "abc@gmail.com"
        data = {"email": email_shared_with}
        url = URLS.SHOPPING_LIST_SHARE_URL.format(pk=shopping_list.pk)
        response = authenticated_api_client.put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
        assert response.data == {"detail": "User not found."}

    def test_share_shopping_list_to_self(
        self,
        authenticated_api_client: APIClient,
        shopping_list: ShoppingList,
        authenticated_user: CustomUser,
    ) -> None:
        email_shared_with = authenticated_user.email
        data = {"email": email_shared_with}
        url = URLS.SHOPPING_LIST_SHARE_URL.format(pk=shopping_list.pk)
        response = authenticated_api_client.put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
        assert response.data == {"detail": "You cannot share the list with yourself."}

    def test_ignore_subsequent_shares(
        self,
        authenticated_api_client: APIClient,
        shopping_list: ShoppingList,
        external_user: CustomUser,
    ) -> None:
        email_shared_with = external_user.email
        data = {"email": email_shared_with}
        url = URLS.SHOPPING_LIST_SHARE_URL.format(pk=shopping_list.pk)

        response_first = authenticated_api_client.put(url, data=data)

        assert response_first.status_code == status.HTTP_200_OK, response_first.content
        assert response_first.data == {"detail": "Shopping list shared successfully."}

        response_second = authenticated_api_client.put(url, data=data)

        assert (
            response_second.status_code == status.HTTP_200_OK
        ), response_second.content
        assert response_second.data == {
            "detail": "Shopping list was already shared with {}.".format(
                email_shared_with
            )
        }

    def test_share_someone_elses_shopping_list(
        self,
        authenticated_api_client: APIClient,
        third_user: CustomUser,
        external_user: CustomUser,
    ) -> None:
        shopping_list_owned_by_external_user = create_shopping_list(user=external_user)

        email_shared_with = third_user.email
        data = {"email": email_shared_with}
        url = URLS.SHOPPING_LIST_SHARE_URL.format(
            pk=shopping_list_owned_by_external_user.pk
        )

        response = authenticated_api_client.put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content
        assert response.data == ERRORS.NOT_FOUND_ERROR

    def test_share_shopping_list_not_authenticated(
        self,
        not_authenticated_api_client: APIClient,
        shopping_list: ShoppingList,
        external_user: CustomUser,
    ) -> None:
        email_shared_with = external_user.email
        data = {"email": email_shared_with}
        url = URLS.SHOPPING_LIST_SHARE_URL.format(pk=shopping_list.pk)
        response = not_authenticated_api_client.put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content
        assert response.data == ERRORS.NOT_FOUND_ERROR

    def test_unshare_shopping_list_from_user(
        self,
        authenticated_api_client: APIClient,
        authenticated_user: CustomUser,
        external_user: CustomUser,
    ):
        authenticated_api_client.force_authenticate(user=external_user)
        shopping_list_owned_by_another_user = create_shopping_list(user=external_user)

        shopping_list_owned_by_another_user.shared_with.add(authenticated_user)

        url = URLS.SHOPPING_LIST_UNSHARE_URL.format(
            pk=shopping_list_owned_by_another_user.pk, user_pk=authenticated_user.pk
        )
        response = authenticated_api_client.patch(url)

        assert response.status_code == status.HTTP_200_OK, response.content
        assert response.data["detail"] == "Successfully unshared the shopping list."

    def test_unshare_not_shared_shopping_list(
        self,
        authenticated_api_client: APIClient,
        authenticated_user: CustomUser,
        external_user: CustomUser,
    ):
        shopping_list = create_shopping_list(user=authenticated_user)

        url = URLS.SHOPPING_LIST_UNSHARE_URL.format(
            pk=shopping_list.pk, user_pk=external_user.pk
        )
        response = authenticated_api_client.patch(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
        assert (
            response.data["detail"]
            == "This list is not shared with the specified user."
        )

    def test_unshare_invalid_user(
        self, authenticated_api_client: APIClient, authenticated_user: CustomUser
    ):
        shopping_list = create_shopping_list(user=authenticated_user)

        invalid_user_id = 9999
        url = URLS.SHOPPING_LIST_UNSHARE_URL.format(
            pk=shopping_list.pk, user_pk=invalid_user_id
        )
        response = authenticated_api_client.patch(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
        assert response.data["detail"] == "User not found."

    def test_unshare_without_permission(
        self,
        authenticated_api_client: APIClient,
        authenticated_user: CustomUser,
        external_user: CustomUser,
    ):
        shopping_list = create_shopping_list(user=external_user)

        url = URLS.SHOPPING_LIST_UNSHARE_URL.format(
            pk=shopping_list.pk, user_pk=authenticated_user.pk
        )
        response = authenticated_api_client.patch(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content
        assert response.data == ERRORS.NOT_FOUND_ERROR

    def test_deleting_shopping_list_by_pk(
        self, authenticated_api_client: APIClient, shopping_list: ShoppingList
    ) -> None:
        url = URLS.SHOPPING_LIST_DETAIL_URL.format(pk=shopping_list.pk)
        response = authenticated_api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT, response.data
        assert not ShoppingList.objects.filter(pk=shopping_list.pk).exists()

    def test_delete_non_existent_shopping_list(
        self, authenticated_api_client: APIClient
    ):
        non_existent_shopping_list_pk = 1
        url = URLS.SHOPPING_LIST_DETAIL_URL.format(pk=non_existent_shopping_list_pk)

        response = authenticated_api_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content
        assert response.data == ERRORS.NOT_FOUND_ERROR

    def test_delete_someone_elses_shopping_list(
        self, authenticated_api_client: APIClient, external_user: CustomUser
    ) -> None:
        shopping_list_owned_by_another_user = create_shopping_list(user=external_user)

        url = URLS.SHOPPING_LIST_DETAIL_URL.format(
            pk=shopping_list_owned_by_another_user.pk
        )

        response = authenticated_api_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content
        assert response.data == ERRORS.NOT_FOUND_ERROR

    def test_delete_shared_shopping_list(
        self,
        authenticated_api_client: APIClient,
        authenticated_user: CustomUser,
        external_user: CustomUser,
    ):
        shopping_list_owned_by_another_user = create_shopping_list(user=external_user)

        shopping_list_owned_by_another_user.shared_with.add(authenticated_user)

        url = URLS.SHOPPING_LIST_DETAIL_URL.format(
            pk=shopping_list_owned_by_another_user.pk
        )

        response = authenticated_api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT, response.content
        assert ShoppingList.objects.filter(
            pk=shopping_list_owned_by_another_user.pk
        ).exists()
        assert not shopping_list_owned_by_another_user.shared_with.filter(
            pk=authenticated_user.pk
        ).exists()


@pytest.mark.django_db
class TestItemViewSet:
    def test_add_new_item_to_shopping_list(
        self, authenticated_api_client: APIClient, shopping_list: ShoppingList
    ) -> None:
        url = URLS.ITEM_LIST_URL.format(shopping_list_pk=shopping_list.pk)
        data: Dict[str, str | ItemCategory | ItemUnit | int] = {
            "product": "Beef",
            "category": ItemCategory.MEAT,
            "quantity": 1,
            "unit": ItemUnit.KILOGRAM,
        }
        print(url)

        response = authenticated_api_client.post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED, response.content
        assert response.data["product"] == data["product"]

    @pytest.mark.parametrize(
        "invalid_data, expected_response",
        [
            (
                {
                    "product": "",
                    "quantity": -1,
                    "unit": "invalid_unit",
                    "category": 123,
                    "completed": "true_string",
                },
                {
                    "product": [ERRORS.NOT_BLANK_ERROR],
                    "quantity": [ERRORS.MIN_QUANTITY_ERROR],
                    "unit": [ERRORS.INVALID_CHOICE_ERROR_UNIT],
                    "category": [ERRORS.INVALID_CHOICE_ERROR_CATEGORY],
                    "completed": [ERRORS.INVALID_BOOLEAN_ERROR],
                },
            ),
        ],
    )
    def test_add_item_with_invalid_data_to_shopping_list(
        self,
        authenticated_api_client: APIClient,
        shopping_list: ShoppingList,
        invalid_data: Dict[str, str | int],
        expected_response: Dict[str, List[str]],
    ) -> None:
        url = URLS.ITEM_LIST_URL.format(shopping_list_pk=shopping_list.pk)
        response = authenticated_api_client.post(url, data=invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
        assert response.data == expected_response

    def test_add_item_to_non_existent_shopping_list(
        self, authenticated_api_client: APIClient
    ) -> None:
        non_existent_shopping_list_pk = 1
        url = URLS.ITEM_LIST_URL.format(shopping_list_pk=non_existent_shopping_list_pk)
        data: Dict[str, str | ItemCategory | ItemUnit | int] = {
            "product": "Beef",
            "category": ItemCategory.MEAT,
            "quantity": 1,
            "unit": ItemUnit.KILOGRAM,
        }

        response = authenticated_api_client.post(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content
        assert response.data == ERRORS.SH_LIST_NOT_FOUND_ERROR

    def test_retrieve_item_by_pk_from_shopping_list(
        self, authenticated_api_client: APIClient, shopping_list: ShoppingList
    ) -> None:
        shopping_list_item = create_item(shopping_list=shopping_list)
        url = URLS.ITEM_DETAIL_URL.format(
            shopping_list_pk=shopping_list.pk, item_pk=shopping_list_item.pk
        )

        response = authenticated_api_client.get(url)

        assert response.status_code == status.HTTP_200_OK, response.content
        assert response.data["product"] == shopping_list_item.product

    def test_update_item_by_pk_from_shopping_list(
        self, authenticated_api_client: APIClient, shopping_list: ShoppingList
    ) -> None:
        shopping_list_item = create_item(shopping_list=shopping_list)
        url = URLS.ITEM_DETAIL_URL.format(
            shopping_list_pk=shopping_list.pk, item_pk=shopping_list_item.pk
        )

        data: Dict[str, str | ItemCategory | ItemUnit | int] = {
            "product": "Milk",
            "category": ItemCategory.DAIRY,
            "quantity": 1,
            "unit": ItemUnit.LITER,
        }

        response = authenticated_api_client.put(
            url,
            data=data,
        )

        assert response.status_code == status.HTTP_200_OK, response.content
        assert response.data["quantity"] == data["quantity"]
        assert response.data["unit"] == data["unit"]

    @pytest.mark.parametrize(
        "invalid_data, expected_response",
        [
            (
                {
                    "product": "Milk",
                    "quantity": -1,
                    "unit": "invalid_unit",
                    "category": 123,
                    "completed": "true_string",
                },
                {
                    "quantity": [ERRORS.MIN_QUANTITY_ERROR],
                    "unit": [ERRORS.INVALID_CHOICE_ERROR_UNIT],
                    "category": [ERRORS.INVALID_CHOICE_ERROR_CATEGORY],
                    "completed": [ERRORS.INVALID_BOOLEAN_ERROR],
                },
            ),
        ],
    )
    def test_update_item_with_invalid_data(
        self,
        authenticated_api_client: APIClient,
        shopping_list: ShoppingList,
        invalid_data: Dict[str, str | int],
        expected_response: Dict[str, List[str]],
    ) -> None:
        shopping_list_item = create_item(shopping_list=shopping_list)
        url = URLS.ITEM_DETAIL_URL.format(
            shopping_list_pk=shopping_list.pk, item_pk=shopping_list_item.pk
        )

        response = authenticated_api_client.put(
            url,
            data=invalid_data,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
        assert response.data == expected_response

    def test_retrieve_non_existent_item_from_shopping_list(
        self, authenticated_api_client: APIClient, shopping_list: ShoppingList
    ) -> None:
        non_existing_item_pk = 1
        url = URLS.ITEM_DETAIL_URL.format(
            shopping_list_pk=shopping_list.pk, item_pk=non_existing_item_pk
        )
        response = authenticated_api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content
        assert response.data == ERRORS.NOT_FOUND_ERROR

    def test_delete_item_by_pk_from_shopping_list(
        self, authenticated_api_client: APIClient, shopping_list: ShoppingList
    ) -> None:
        shopping_list_item = create_item(shopping_list=shopping_list)
        url = URLS.ITEM_DETAIL_URL.format(
            shopping_list_pk=shopping_list.pk, item_pk=shopping_list_item.pk
        )

        assert len(shopping_list.items.all()) == 1

        response = authenticated_api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT, response.content
        assert len(shopping_list.items.all()) == 0

    def test_delete_non_existent_item_from_shopping_list(
        self, authenticated_api_client: APIClient, shopping_list: ShoppingList
    ) -> None:
        non_existing_item_pk = 1
        url = URLS.ITEM_DETAIL_URL.format(
            shopping_list_pk=shopping_list.pk, item_pk=non_existing_item_pk
        )

        response = authenticated_api_client.delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.content
        assert response.data == ERRORS.NOT_FOUND_ERROR
