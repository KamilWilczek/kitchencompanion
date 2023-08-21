const BASE_URL = 'http://127.0.0.1:8000/shoppinglist/';

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
    return await fetch(`${BASE_URL}create-update/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
};