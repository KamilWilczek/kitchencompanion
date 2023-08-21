import React from 'react';
import Item from './Item';

const ItemsList = ({ items, onItemClick, onCompletionChange }) => {
    return (
        <div className='items-list'>
            {items && items.map(item => (
                <Item 
                    key={item.id} 
                    item={item} 
                    onItemClick={onItemClick} 
                    onCompletionChange={onCompletionChange} 
                />
            ))}
        </div>
    );
};

export default ItemsList;