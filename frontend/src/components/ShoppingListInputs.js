import React from 'react';

const ShoppingListInputs = ({ name, description, onNameChange, onDescriptionChange }) => {
    return (
        <>
            <input
                type="text"
                placeholder="Shopping List Name"
                onChange={onNameChange}
                value={name}
            />
    
            <input
                type="text"
                placeholder="Description"
                onChange={onDescriptionChange}
                value={description}
            />
        </>
    );
}

export default ShoppingListInputs;