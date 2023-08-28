import React from 'react';
import { Link } from 'react-router-dom';

interface ShoppingListProps {
    shoppingList: {
        id: string | number;
        name: string;
        updated: string | Date;
        items_count: number;
    };
}

const getDate = (shoppingList: ShoppingListProps["shoppingList"]): string => {
    return new Date(shoppingList.updated).toLocaleDateString();
}

const getName = (shoppingList: ShoppingListProps["shoppingList"]): string => {
    return shoppingList.name;
}

const ShoppingList: React.FC<ShoppingListProps> = ({ shoppingList }) => {
    return (
        <Link to={`shoppinglist/${shoppingList.id}/edit/`}>
            <div className='shoppinglists-list-item'>
                <h3>{getName(shoppingList)}</h3>
                <p><span>{getDate(shoppingList)}</span></p>
                <p>Items count: {shoppingList.items_count}</p>
            </div>
        </Link>
    );
}

export default ShoppingList;