import React from 'react';
import Item from './Item';

interface ItemProps {
    id: string | number;
    product: string;
    quantity?: string | number;
    unit?: string;
    category?: string;
    completed?: boolean;
    note?: string;
}

interface ItemsListProps {
    items: ItemProps[];
    onItemClick: (id: string | number) => void;
    onCompletionChange: (item: ItemProps) => void;
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