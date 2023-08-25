export interface ShoppingListItem {
    id: string | number;
    product: string;
    quantity?: string | number;
    unit?: string;
    category?: string;
    note?: string;
    completed: boolean;
}

export interface ShoppingList {
    id: string | number;
    name: string;
    description?: string;
    items: ShoppingListItem[];
    updated: Date;
    items_count: number;
}

export interface NewShoppingList {
    name: string;
    description?: string;
    items: ShoppingListItem[];
}