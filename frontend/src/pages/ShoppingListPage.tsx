import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import ItemsList from '../components/ItemsList';
import ItemModal from '../components/ItemModal';
import {
    fetchShoppingListItem,
    updateShoppingListItem,
    createShoppingListItem,
    deleteShoppingListItem
} from '../utils/apiUtils'
import { categories, units } from '../utils/constants';
import useShoppingList from '../hooks/useShoppingList';
import ShoppingListHeader from '../components/ShoppingListHeader';
import ShoppingListInputs from '../components/ShoppingListInputs';
import { ShoppingListItem } from '../utils/types';

const ShoppingListPage: React.FC = () => {
    // TODO: how to handle if id is undefined
    const { id: shoppingListId  } = useParams<{ id?: string }>();
    const defaultItem: ShoppingListItem = {
        id: -1,
        product: '',
        quantity: '',
        unit: '',
        category: '',
        note: '',
        completed: false
    };
    const [shoppingList, updateShoppingListState, saveShoppingList, removeShoppingList] = useShoppingList(shoppingListId);
    const [selectedItem, setSelectedItem] = useState<ShoppingListItem>(defaultItem);
    const [isModalOpen, setShowModal] = useState<boolean>(false);


    const handleItemSelection = async (shoppingListItemId: number) => {
        if (shoppingListId) {  // Make sure id is not undefined
            const data = await fetchShoppingListItem(shoppingListId, shoppingListItemId);
            setSelectedItem(data);
            setShowModal(true);
        }
    };

    const saveSelectedItemChanges = async () => {
        if (selectedItem && shoppingListId) {
            const response = await updateShoppingListItem(shoppingListId, selectedItem.id, selectedItem);
            if (response.ok) {
                const updatedItem: ShoppingListItem = await response.json();
                const updatedItems = shoppingList.items.map(i => i.id === updatedItem.id ? updatedItem : i);
                updateShoppingListState({ items: updatedItems });
                setShowModal(false);
            }
        }
    };

    const toggleItemCompletionStatus = async (item: ShoppingListItem) => {
        const updatedItem = { ...item, completed: !item.completed };
        if (shoppingListId) {
            const response = await updateShoppingListItem(shoppingListId, item.id, updatedItem);
            if (response.ok) {
                const updatedItems = shoppingList.items.map(i => i.id === updatedItem.id ? updatedItem : i);
                updateShoppingListState({ items: updatedItems });
            }
        }
    };

    const saveNewItemDetails = async () => {
        if (shoppingListId && selectedItem) {
            const response = await createShoppingListItem(shoppingListId, selectedItem);
            if (response.ok) {
                const newItem: ShoppingListItem = await response.json();
                const updatedItems = [...shoppingList.items, newItem];
                updateShoppingListState({ items: updatedItems });
                setShowModal(false);
            }
        }
    };

    const initiateNewItemAddition = () => {
        setSelectedItem(defaultItem);
        setShowModal(true);
    };

    const deleteSelectedItem = async (shoppingListItemId: number) => {
        if (shoppingListId) {
            await deleteShoppingListItem(shoppingListId, shoppingListItemId);
            const updatedItems = shoppingList.items.filter(item => item.id !== shoppingListItemId);
            updateShoppingListState({ items: updatedItems });
            setShowModal(false)
        }
;
    };

    return (
        <div className='shoppinglist'>
            <ShoppingListHeader 
                shoppingListId ={shoppingListId || 'defaultIdValue'}
                shoppingList={shoppingList}
                onSave={saveShoppingList}
                onDelete={removeShoppingList}
            />


            <ShoppingListInputs 
                name={shoppingList?.name}
                description={shoppingList?.description || ''}
                onNameChange={(e) => updateShoppingListState({ name: e.target.value })}
                onDescriptionChange={(e) => updateShoppingListState({ description: e.target.value })}
            />

            <hr />

            {shoppingListId !== 'new' && <button onClick={initiateNewItemAddition}>Add item</button>}

            <div className='items-list'>
                <ItemsList 
                    items={shoppingList?.items || []} 
                    onItemClick={handleItemSelection} 
                    onCompletionChange={toggleItemCompletionStatus} 
                />
            </div>
            {isModalOpen && (
                <ItemModal 
                    isModalOpen={isModalOpen}
                    onClose={() => setShowModal(false)}
                    selectedItem={selectedItem}
                    setSelectedItem={setSelectedItem}
                    units={units}
                    categories={categories}
                    onSaveChanges={selectedItem?.id === -1 ? saveNewItemDetails : saveSelectedItemChanges}
                    onDelete={deleteSelectedItem}
                />
            )}
        </div>
    );
}

export default ShoppingListPage;