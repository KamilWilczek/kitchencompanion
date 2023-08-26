import React from 'react';
import { ReactComponent as ArrowLeft } from '../assets/arrow-left.svg';
import { ShoppingList, NewShoppingList } from '../utils/types';

interface ShoppingListHeaderProps {
    id: string | number;
    shoppingList: ShoppingList | NewShoppingList;
    onSave: (list: ShoppingList | NewShoppingList) => Promise<void>;
    onDelete: () => void;
}

const ShoppingListHeader: React.FC<ShoppingListHeaderProps> = ({ id, shoppingList, onSave, onDelete }) => {
    return (
        <div className='shoppinglist-header'>
            <h3>
                <ArrowLeft onClick={() => onSave(shoppingList)} />
            </h3>
            {id !== 'new' ? (
                <button onClick={onDelete}>Delete</button>
            ) : (
                <button onClick={() => onSave(shoppingList)}>Done</button>
            )}
        </div>
    );
}

export default ShoppingListHeader;