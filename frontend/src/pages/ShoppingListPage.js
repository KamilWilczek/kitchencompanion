import React, { useState }  from 'react'
import { useParams } from 'react-router-dom';
import { ReactComponent as ArrowLeft } from '../assets/arrow-left.svg'
import ItemsList from '../components/ItemsList';
import ItemModal from '../components/ItemModal';
import { fetchShoppingListItem, updateShoppingListItem, createShoppingListItem, deleteShoppingListItem } from '../utils/apiUtils';
import { categories, units } from '../utils/constants';
import useShoppingList from '../hooks/useShoppingList';

const ShoppingListPage = () => {
    let {id} = useParams();
    const [shoppingList, updateShoppingListState, saveShoppingList, removeShoppingList] = useShoppingList(id);
    const [selectedItem, setSelectedItem] = useState(null);
    const [isModalOpen, setShowModal] = useState(false);

    const handleItemSelection = async (itemId) => {
        const data = await fetchShoppingListItem(id, itemId);
        setSelectedItem(data);
        setShowModal(true);
    };

    const saveSelectedItemChanges = async () => {
        if (selectedItem) {
            const response = await updateShoppingListItem(id, selectedItem.id, selectedItem);
            if (response.ok) {
                setShowModal(false);
            }
        }
    };

    const toggleItemCompletionStatus = async (item) => {
        const updatedItem = { ...item, completed: !item.completed };
        const response = await updateShoppingListItem(id, item.id, updatedItem);
        if (response.ok) {
            const updatedItems = shoppingList.items.map(i => i.id === updatedItem.id ? updatedItem : i);
            updateShoppingListState({ items: updatedItems });
        }
    };

    const saveNewItemDetails = async () => {
        const response = await createShoppingListItem(id, selectedItem);
        if (response.ok) {
            const newItem = await response.json();
            const updatedItems = [...shoppingList.items, newItem];
            updateShoppingListState({ items: updatedItems });
            setShowModal(false);
        }
    };

    const initiateNewItemAddition = () => {
        setSelectedItem({});  // Initialize to an empty object
        setShowModal(true);
    };

    const deleteSelectedItem = async (itemId) => {
        await deleteShoppingListItem(id, itemId);
        const updatedItems = shoppingList.items.filter(item => item.id !== itemId);
        updateShoppingListState({ items: updatedItems });
        setShowModal(false);
    };

    return (
        <div className='shoppinglist'>
            <div className='shoppinglist-header'>
                <h3>
                    <ArrowLeft onClick={() => saveShoppingList(shoppingList)} />
                </h3>
                {id !== 'new' ? (
                    <button onClick={() => removeShoppingList()}>Delete</button>
                ) : (
                    <button onClick={() => saveShoppingList(shoppingList)}>Done</button>
                )}
            </div>
            <input
                type="text"
                placeholder="Shopping List Name"
                onChange={(e) => updateShoppingListState({ name: e.target.value })}
                value={shoppingList?.name}
            />
    
            <input
                type="text"
                placeholder="Description"
                onChange={(e) => updateShoppingListState({ description: e.target.value })}
                value={shoppingList?.description}
            />
    
            <hr />  {/* Horizontal rule to separate sections */}
    
            {id !== 'new' && <button onClick={initiateNewItemAddition}>Add item</button>}
    
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
                    onSaveChanges={selectedItem?.id ? saveSelectedItemChanges : saveNewItemDetails}
                    onDelete={deleteSelectedItem}
                />
            )}
        </div>
    )
}

export default ShoppingListPage