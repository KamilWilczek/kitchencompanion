import React from 'react';
import { ReactComponent as ArrowLeft } from '../assets/arrow-left.svg'

const ShoppingListHeader = ({ id, onSave, onDelete }) => {
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