import React from 'react';
import Item from './Item';
import { ShoppingListItem } from '../utils/types';


interface ItemsListProps {
    items: ShoppingListItem[];
    onItemClick: (id: number) => void;
    onCompletionChange: (item: ShoppingListItem) => void;
}

const ItemsList: React.FC<ItemsListProps> = ({ items, onItemClick, onCompletionChange }) => {
    return (
        <div className='items-list'>
            {items && items.map(item => (
                <Item 
                    key={item.id} 
                    item={{ ...item, completed: item.completed || false , category: item.category || undefined}}
                    onItemClick={onItemClick} 
                    onCompletionChange={onCompletionChange} 
                />
            ))}
        </div>
    );
};

export default ItemsList;