import React from 'react';

interface ShoppingListInputsProps {
    name: string;
    description: string;
    onNameChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
    onDescriptionChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const ShoppingListInputs: React.FC<ShoppingListInputsProps> = ({ name, description, onNameChange, onDescriptionChange }) => {
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