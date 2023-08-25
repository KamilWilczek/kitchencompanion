import { ShoppingList } from "./types";

const BASE_URL = 'http://127.0.0.1:8000/shoppinglist/';


interface ShoppingListItem {
    id: string | number;
    product: string;
    quantity?: string | number;
    unit?: string;
    category?: string;
    note?: string;
    completed: boolean;
}

interface NewShoppingList {
    name: string;
    // ... other fields, but not the ID
}

export const fetchShoppingLists = async (): Promise<ShoppingList[]> => {
    const response = await fetch(`${BASE_URL}`);
    return await response.json();
};

export const fetchShoppingList = async (id: number | string): Promise<ShoppingList> => {
    const response = await fetch(`${BASE_URL}${id}/edit/`);
    return await response.json();
};

// Use the ShoppingList type when you're updating a shopping list
export const updateShoppingList = async (id: number | string, data: ShoppingList): Promise<Response> => {
    return await fetch(`${BASE_URL}${id}/edit/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
};

export const deleteShoppingList = async (id: number | string): Promise<Response> => {
    return await fetch(`${BASE_URL}${id}/delete/`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
    });
};

export const createShoppingList = async (data: NewShoppingList): Promise<Response> => {
    return await fetch(`${BASE_URL}create-update/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
};

// Use the ShoppingListItem type for operations related to individual items
export const fetchShoppingListItem = async (listId: string | number, itemId: string | number): Promise<ShoppingListItem> => {
    const response = await fetch(`${BASE_URL}${listId}/item/${itemId}/`);
    return await response.json();
};

export const updateShoppingListItem = async (listId: string, itemId: string | number, data: ShoppingListItem | NewShoppingList): Promise<Response> => {
    return await fetch(`${BASE_URL}${listId}/item/${itemId}/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
};

export const createShoppingListItem = async (listId: string, data: ShoppingListItem): Promise<Response> => {
    return await fetch(`${BASE_URL}${listId}/item/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
};

export const deleteShoppingListItem = async (listId: string, itemId: string | number): Promise<Response> => {
    return await fetch(`${BASE_URL}${listId}/item/${itemId}/delete/`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
    });
};
