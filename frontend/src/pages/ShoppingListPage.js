import React, { useState, useEffect }  from 'react'
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import { ReactComponent as ArrowLeft } from '../assets/arrow-left.svg'
import ItemsList from '../components/ItemsList';
import ItemModal from '../components/ItemModal';
import { fetchShoppingList, updateShoppingList, createShoppingList, deleteShoppingList } from '../utils/apiUtils';

const ShoppingListPage = () => {
    let {id} = useParams();
    let [shoppingList, setshoppingList] = useState(null)
    const [selectedItem, setSelectedItem] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const navigate = useNavigate();
    const categories = [
        "fruits and vegetables",
        "meat",
        "diary",
        "dry goods",
        "alcohols",
        "medicine",
        "pet goods",
        "baby goods",
        "domestic detergents",
        "ready-cook meals",
        "hygiene",
        "coffee & tea",
        "frozen foods",
        "garden and tinkering",
        "bread",
        "preserves",
        "spices, sauces, additives",
        "fishes and seafood",
        "sweets and snacks",
        "fats",
        "water and drinks",
        "dried fruit and nuts",
        "fresh herbs",
        "canned food",
        "other"
    ];
    const units = ["pcs", "pkgs", "kg", "g", "l", "ml"];

    const sortItems = (items) => {
        return items.sort((a, b) => {
            // First, sort by completion status
            if (a.completed !== b.completed) return a.completed ? 1 : -1;
    
            // Then, sort alphabetically by product name
            if (a.product.toLowerCase() < b.product.toLowerCase()) return -1;
            if (a.product.toLowerCase() > b.product.toLowerCase()) return 1;
            return 0;
        });
    };
    
    useEffect(() => {
        if (id !== 'new') {
            fetchShoppingList(id).then(data => {
                if (data.items) {
                    data.items = sortItems(data.items);
                }
                setshoppingList(data);
            });
        } else {
            setshoppingList({ name: "", description: "" });
        }
    }, [id]);

    const handleSubmit = () => {
        if (id === 'new') {
            createShoppingList({...shoppingList, 'updated': new Date() }).then(() => navigate('/'));
        } else if (shoppingList.name.trim() === '') {
            deleteShoppingList(id).then(() => navigate('/'));
        } else {
            updateShoppingList(id, shoppingList).then(() => navigate('/'));
        }
    }

    let handleChange = (key, value) => {
        setshoppingList(prevList => ({ ...prevList, [key]: value }));
    }

    const handleItemClick = async (itemId) => {
        const response = await fetch(`http://127.0.0.1:8000/shoppinglist/${id}/item/${itemId}/`);
        const data = await response.json();
        setSelectedItem(data);
        setShowModal(true);
    };

    const handleItemUpdate = async () => {
        if (selectedItem) {
            const response = await fetch(`http://127.0.0.1:8000/shoppinglist/${id}/item/${selectedItem.id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(selectedItem)
            });
            if (response.ok) {
                const updatedItems = shoppingList.items.map(item => 
                    item.id === selectedItem.id ? selectedItem : item
                );
                setshoppingList(prevState => ({ ...prevState, items: sortItems(updatedItems) }));
                setShowModal(false);
            }
        }
    };

    const handleCompletionChange = async (item) => {
        const updatedItem = { ...item, completed: !item.completed };
    
        // Update in the backend
        const response = await fetch(`http://127.0.0.1:8000/shoppinglist/${id}/item/${item.id}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedItem)
        });
    
        if (response.ok) {
            const updatedItems = shoppingList.items.map(i => 
                i.id === item.id ? updatedItem : i
            );
            setshoppingList(prevState => ({ ...prevState, items: sortItems(updatedItems) }));
        }
    };

    const handleNewItemSave = async () => {
        const response = await fetch(`http://127.0.0.1:8000/shoppinglist/${id}/item/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(selectedItem)
        });
    
        if (response.ok) {
            const newItem = await response.json();
    
            const updatedItems = [...shoppingList.items, newItem];
            setshoppingList(prevState => ({ ...prevState, items: updatedItems }));
            setShowModal(false);
        }
    };

    const handleAddItem = () => {
        setSelectedItem({});  // Initialize to an empty object
        setShowModal(true);
    };

    const handleItemDelete = async (itemId) => {
        const response = await fetch(`http://127.0.0.1:8000/shoppinglist/${id}/item/${itemId}/delete/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
    
        if (response.ok) {
            // Remove the deleted item from the shopping list state
            const updatedItems = shoppingList.items.filter(item => item.id !== itemId);
            
            setshoppingList(prevState => ({ ...prevState, items: updatedItems }));
            
            // Close the modal
            setShowModal(false);
        } else {
            // Handle the error appropriately
            console.error("Failed to delete the item.");
        }
    };

    return (
        <div className='shoppinglist'>
            <div className='shoppinglist-header'>
                <h3>
                    <ArrowLeft onClick={handleSubmit} />
                </h3>
                {id !== 'new' ? (
                    <button onClick={deleteShoppingList}>Delete</button>
                ) : (
                    <button onClick={handleSubmit}>Done</button>
                )}
            </div>
            <input
                type="text"
                placeholder="Shopping List Name"
                onChange={(e) => handleChange('name', e.target.value)}
                value={shoppingList?.name}
            />
    
            <input
                type="text"
                placeholder="Description"
                onChange={(e) => handleChange('description', e.target.value)}
                value={shoppingList?.description}
            />
    
            <hr />  {/* Horizontal rule to separate sections */}
    
            {id !== 'new' && <button onClick={handleAddItem}>Add item</button>}
    
            <div className='items-list'>
                <ItemsList 
                    items={shoppingList?.items} 
                    onItemClick={handleItemClick} 
                    onCompletionChange={handleCompletionChange} 
                />
            </div>
            {showModal && (
                <ItemModal 
                    showModal={showModal}
                    onClose={() => setShowModal(false)}
                    selectedItem={selectedItem}
                    setSelectedItem={setSelectedItem}
                    units={units}
                    categories={categories}
                    onSaveChanges={selectedItem?.id ? handleItemUpdate : handleNewItemSave}
                    onDelete={handleItemDelete}
                />
            )}
        </div>
    )
}

export default ShoppingListPage