import { ShoppingList, ShoppingListItem, NewShoppingList } from "./types";

const BASE_URL = 'http://127.0.0.1:8000/shoppinglist/';


export const fetchShoppingLists = async (): Promise<ShoppingList[]> => {
    const response = await fetch(`${BASE_URL}`);
    return await response.json();
};

export const fetchShoppingList = async (shoppingListId : number | string): Promise<ShoppingList> => {
    const response = await fetch(`${BASE_URL}${shoppingListId }/edit/`);
    return await response.json();
};

export const updateShoppingList = async (shoppingListId : number | string, data: ShoppingList): Promise<Response> => {
    return await fetch(`${BASE_URL}${shoppingListId }/edit/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
};

export const deleteShoppingList = async (shoppingListId : number | string): Promise<Response> => {
    return await fetch(`${BASE_URL}${shoppingListId }/delete/`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
    });
};

export const createShoppingList = async (data: NewShoppingList): Promise<Response> => {
    return await fetch(`${BASE_URL}create/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
};

export const fetchShoppingListItem = async (shoppingListId : string | number, shoppingListItemId: number): Promise<ShoppingListItem> => {
    const response = await fetch(`${BASE_URL}${shoppingListId }/item/${shoppingListItemId}/`);
    return await response.json();
};

export const updateShoppingListItem = async (shoppingListId : string, shoppingListItemId: string | number, data: ShoppingListItem | NewShoppingList): Promise<Response> => {
    return await fetch(`${BASE_URL}${shoppingListId }/item/${shoppingListItemId}/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
};

export const createShoppingListItem = async (shoppingListId : string, data: ShoppingListItem): Promise<Response> => {
    return await fetch(`${BASE_URL}${shoppingListId }/item/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
};

export const deleteShoppingListItem = async (shoppingListId : string, shoppingListItemId: string | number): Promise<Response> => {
    return await fetch(`${BASE_URL}${shoppingListId }/item/${shoppingListItemId}/delete/`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
    });
};
