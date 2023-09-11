class URLS:
    SHOPPING_LIST_URL = "/shoppinglist"
    SHOPPING_LIST_CREATE_URL = f"{SHOPPING_LIST_URL}/create/"
    SHOPPING_LIST_EDIT_URL = f"{SHOPPING_LIST_URL}/{{pk}}/edit/"
    SHOPPING_LIST_DELETE_URL = f"{SHOPPING_LIST_URL}/{{pk}}/delete/"
    ITEM_URL = f"{SHOPPING_LIST_URL}/{{shopping_list_pk}}/item/"
    ITEM_DETAIL_URL = f"{SHOPPING_LIST_URL}/{{shopping_list_pk}}/item/{{item_pk}}/"
    ITEM_DELETE_URL = (
        f"{SHOPPING_LIST_URL}/{{shopping_list_pk}}/item/{{item_pk}}/delete/"
    )
