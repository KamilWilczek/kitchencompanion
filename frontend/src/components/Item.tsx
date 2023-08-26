import React from 'react';

interface ItemProps {
  item: {
    id: number;
    product: string;
    completed: boolean;
    quantity?: string | number;
    unit?: string;
    category: string | undefined;
    note?: string;
  };
  onItemClick: (id: number) => void;
  onCompletionChange: (item: ItemProps['item']) => void;
}

const Item: React.FC<ItemProps> = ({ item, onItemClick, onCompletionChange }) => {
    return (
        <div 
            key={item.id} 
            className={`item ${item.completed ? 'completed' : ''}`} 
            onClick={() => onItemClick(item.id)}
        >
            <div>
                <div className='item-left'>
                    <div className='item-name'>{item.product}</div>
                </div>
                <div className='item-right'>
                    {item.quantity && <div className='item-quantity'>{item.quantity}</div>}
                    {item.unit && <div className='item-unit'>{item.unit}</div>}
                </div>
                <div className='item-category'>{item.category}</div>
                <input 
                    type="checkbox" 
                    checked={item.completed} 
                    onClick={(e) => {
                        e.stopPropagation();
                        onCompletionChange(item);
                    }} 
                />
            </div>
            <div>
                {item.note && <div className='item-note'>{item.note}</div>}
            </div>
        </div>
    );
};

export default Item;