import React from 'react';

interface ItemModalProps {
    isModalOpen: boolean;
    onClose: () => void;
    selectedItem: {
        id?: string | number;
        product?: string;
        quantity?: string | number;
        unit?: string;
        category?: string;
        note?: string;
    };
    setSelectedItem: (item: ItemModalProps['selectedItem']) => void;
    units: string[];
    categories: string[];
    onSaveChanges: () => void;
    onDelete: (id: string | number) => void;
}


const ItemModal: React.FC<ItemModalProps> = ({ 
    isModalOpen, 
    onClose, 
    selectedItem, 
    setSelectedItem, 
    units, 
    categories, 
    onSaveChanges,
    onDelete 
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
                    onChange={(e) => setSelectedItem(prev => ({ ...prev, product: e.target.value }))}
                />
                <input 
                    type="text"
                    value={selectedItem?.quantity || ''}
                    onChange={(e) => setSelectedItem(prev => ({ ...prev, quantity: e.target.value }))}
                />
                <select 
                    value={selectedItem.unit || ''} 
                    onChange={(e) => {setSelectedItem(prev => ({ ...prev, unit: e.target.value }))}}
                >
                    <option value="" disabled selected>Select a unit</option>
                    {units.map(unit => (
                        <option key={unit} value={unit}>{unit}</option>
                    ))}
                </select>
                <select 
                    value={selectedItem.category || ''} 
                    onChange={(e) => {setSelectedItem(prev => ({ ...prev, category: e.target.value }))}}
                >
                    <option value="" disabled selected>Select a category</option>
                    {categories.map(category => (
                        <option key={category} value={category}>{category}</option>
                    ))}
                </select>
                <textarea 
                    type="text"
                    value={selectedItem?.note || ''}
                    onChange={(e) => setSelectedItem(prev => ({ ...prev, note: e.target.value }))}
                />

                <button onClick={onSaveChanges}>
                    Save Changes
                </button>
                {selectedItem && selectedItem.id && (
                    <button onClick={() => onDelete(selectedItem.id)}>Delete</button>
                )}
            </div>
        </div>
    );
};

export default ItemModal;