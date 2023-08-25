import React from 'react';

interface ItemModalProps {
    categories: string[];
    isModalOpen: boolean;
    selectedItem: {
        id?: string | number;
        product?: string;
        quantity?: string | number;
        unit?: string;
        category?: string;
        note?: string;
    };
    units: string[];
    onClose: () => void;
    onDelete: (id: string | number) => void;
    onSaveChanges: () => void;
    setSelectedItem: (item: ItemModalProps['selectedItem']) => void;
}


const ItemModal: React.FC<ItemModalProps> = ({ 
    categories, 
    isModalOpen, 
    selectedItem, 
    units, 
    onClose, 
    onDelete, 
    onSaveChanges,
    setSelectedItem 
}) => {
    return (
        <div className={`modal ${isModalOpen ? 'show' : 'hide'}`}>
            <div className="modal-content">
                {/* Close Button */}
                <button onClick={onClose}>Close</button>

                {/* Fields for editing */}
                <input 
                    type="text"
                    value={selectedItem?.product || ''}
                    onChange={(e) => {
                        const updatedItem = { ...selectedItem, product: e.target.value };
                        setSelectedItem(updatedItem);
                    }}
                />
                <input 
                    type="text"
                    value={selectedItem?.quantity || ''}
                    onChange={(e) => {
                        const updatedItem = { ...selectedItem, quantity: e.target.value };
                        setSelectedItem(updatedItem);
                    }}
                />
                <select 
                    value={selectedItem.unit || ''} 
                    onChange={(e) => {
                        const updatedItem = { ...selectedItem, unit: e.target.value };
                        setSelectedItem(updatedItem);
                    }}
                >
                    <option value="" disabled selected>Select a unit</option>
                    {units.map(unit => (
                        <option key={unit} value={unit}>{unit}</option>
                    ))}
                </select>
                <select 
                    value={selectedItem.category || ''} 
                    onChange={(e) => {
                        const updatedItem = { ...selectedItem, category: e.target.value };
                        setSelectedItem(updatedItem);
                    }}
                >
                    <option value="" disabled selected>Select a category</option>
                    {categories.map(category => (
                        <option key={category} value={category}>{category}</option>
                    ))}
                </select>
                <textarea 
                    value={selectedItem?.note || ''}
                    onChange={(e) => {
                        const updatedItem = { ...selectedItem, note: e.target.value };
                        setSelectedItem(updatedItem);
                    }}
                />

                <button onClick={onSaveChanges}>
                    Save Changes
                </button>
                {selectedItem && selectedItem.id && (
                    <button onClick={() => onDelete(selectedItem.id!)}>Delete</button>
                )}
            </div>
        </div>
    );
};

export default ItemModal;