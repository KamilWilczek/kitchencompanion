const BASE_URL = 'http://127.0.0.1:8000/shoppinglist/';

export const fetchShoppingLists = async () => {
    const response = await fetch(`${BASE_URL}`);
    return await response.json()
};

export const fetchShoppingList = async (id) => {
    const response = await fetch(`${BASE_URL}${id}/edit/`);
    return await response.json();
};

export const updateShoppingList = async (id, data) => {
    return await fetch(`${BASE_URL}${id}/edit/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
};

export const deleteShoppingList = async (id) => {
    return await fetch(`${BASE_URL}${id}/delete/`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
    });
};

export const createShoppingList = async (data) => {
    console.log("Data before sending:", data);
    return await fetch(`${BASE_URL}create-update/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    
};

export const fetchShoppingListItem = async (listId, itemId) => {
    const response = await fetch(`${BASE_URL}${listId}/item/${itemId}/`);
    return await response.json();
};

export const updateShoppingListItem = async (listId, itemId, data) => {
    return await fetch(`${BASE_URL}${listId}/item/${itemId}/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
};

export const createShoppingListItem = async (listId, data) => {
    return await fetch(`${BASE_URL}${listId}/item/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
};

export const deleteShoppingListItem = async (listId, itemId) => {
    return await fetch(`${BASE_URL}${listId}/item/${itemId}/delete/`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
    });
};