const BASE_URL = 'http://127.0.0.1:8000/shoppinglist/';

export const fetchShoppingLists = async (): Promise<any[]> => {
    const response = await fetch(`${BASE_URL}`);
    return await response.json();
};

export const fetchShoppingList = async (id: string): Promise<any> => {
    const response = await fetch(`${BASE_URL}${id}/edit/`);
    return await response.json();
};

export const updateShoppingList = async (id: string, data: any): Promise<Response> => {
    return await fetch(`${BASE_URL}${id}/edit/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
};

export const deleteShoppingList = async (id: string): Promise<Response> => {
    return await fetch(`${BASE_URL}${id}/delete/`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
    });
};

export const createShoppingList = async (data: any): Promise<Response> => {
    return await fetch(`${BASE_URL}create-update/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
};

export const fetchShoppingListItem = async (listId: string, itemId: string): Promise<any> => {
    const response = await fetch(`${BASE_URL}${listId}/item/${itemId}/`);
    return await response.json();
};

export const updateShoppingListItem = async (listId: string, itemId: string, data: any): Promise<Response> => {
    return await fetch(`${BASE_URL}${listId}/item/${itemId}/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
};

export const createShoppingListItem = async (listId: string, data: any): Promise<Response> => {
    return await fetch(`${BASE_URL}${listId}/item/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
};

export const deleteShoppingListItem = async (listId: string, itemId: string): Promise<Response> => {
    return await fetch(`${BASE_URL}${listId}/item/${itemId}/delete/`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
    });
};
