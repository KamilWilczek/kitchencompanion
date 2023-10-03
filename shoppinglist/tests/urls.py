class URLS:
    SHOPPING_LIST_URL = "/shoppinglist"
    SHOPPING_LIST_DETAIL_URL = f"{SHOPPING_LIST_URL}/{{pk}}/"
    SHOPPING_LIST_SHARE_URL = f"{SHOPPING_LIST_URL}/{{pk}}/share/"
    SHOPPING_LIST_UNSHARE_URL = f"{SHOPPING_LIST_URL}/{{pk}}/unshare/{{user_pk}}/"
    ITEM_URL = f"{SHOPPING_LIST_URL}/{{shopping_list_pk}}/item/"
    ITEM_DETAIL_URL = f"{SHOPPING_LIST_URL}/{{shopping_list_pk}}/item/{{item_pk}}/"
    ITEM_DELETE_URL = (
        f"{SHOPPING_LIST_URL}/{{shopping_list_pk}}/item/{{item_pk}}/delete/"
    )
