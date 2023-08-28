import React from 'react';
import { ReactComponent as ArrowLeft } from '../assets/arrow-left.svg';
import { ShoppingList, NewShoppingList } from '../utils/types';

interface ShoppingListHeaderProps {
    shoppingListId : string | number;
    shoppingList: ShoppingList | NewShoppingList;
    onSave: (list: ShoppingList | NewShoppingList) => Promise<void>;
    onDelete: () => void;
}

const ShoppingListHeader: React.FC<ShoppingListHeaderProps> = ({ shoppingListId , shoppingList, onSave, onDelete }) => {
    return (
        <div className='shoppinglist-header'>
            <h3>
                <ArrowLeft onClick={() => onSave(shoppingList)} />
            </h3>
            {shoppingListId  !== 'new' ? (
                <button onClick={onDelete}>Delete</button>
            ) : (
                <button onClick={() => onSave(shoppingList)}>Done</button>
            )}
        </div>
    );
}

export default ShoppingListHeader;