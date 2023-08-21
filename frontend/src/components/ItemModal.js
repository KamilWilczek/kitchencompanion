import React from 'react';


const ItemModal = ({ 
    showModal, 
    onClose, 
    selectedItem, 
    setSelectedItem, 
    units, 
    categories, 
    onSaveChanges,
    onDelete 
}) => {
    return (
        <div className={`modal ${showModal ? 'show' : 'hide'}`}>
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
                    value={selectedItem?.unit || ''}
                    onChange={(e) => setSelectedItem(prev => ({ ...prev, unit: e.target.value }))}
                >
                    {units.map(unit => (
                        <option key={unit} value={unit}>
                            {unit.charAt(0).toUpperCase() + unit.slice(1)}
                        </option>
                    ))}
                </select>
                <select
                    value={selectedItem?.category || ''}
                    onChange={(e) => setSelectedItem(prev => ({ ...prev, category: e.target.value }))}
                >
                    {categories.map(category => (
                        <option key={category} value={category}>
                            {category.charAt(0).toUpperCase() + category.slice(1)}
                        </option>
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