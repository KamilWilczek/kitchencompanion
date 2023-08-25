import React from 'react';
import { ReactComponent as ArrowLeft } from '../assets/arrow-left.svg';

interface ShoppingListHeaderProps {
    id: string | number;
    onSave: () => void;
    onDelete: () => void;
}

const ShoppingListHeader: React.FC<ShoppingListHeaderProps> = ({ id, onSave, onDelete }) => {
    return (
        <div className='shoppinglist-header'>
            <h3>
                <ArrowLeft onClick={onSave} />
            </h3>
            {id !== 'new' ? (
                <button onClick={onDelete}>Delete</button>
            ) : (
                <button onClick={onSave}>Done</button>
            )}
        </div>
    );
}

export default ShoppingListHeader;