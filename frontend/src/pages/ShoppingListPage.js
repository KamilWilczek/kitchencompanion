import React, { useState, useEffect }  from 'react'
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import { ReactComponent as ArrowLeft } from '../assets/arrow-left.svg'

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
    

    useEffect(() => {
        if (id === 'new') {
            // Initialize shoppingList for new list creation
            setshoppingList({ name: "", description: "" });
        } else {
            getShoppingList();
        }
    }, [id]);

    let getShoppingList = async () => {
        if (id === 'new') return
        let response = await fetch(`http://127.0.0.1:8000/shoppinglist/${id}/edit/`)
        let data = await response.json()
        setshoppingList(data)
    }

    let updateShoppingList = async () => {
        await fetch(`http://127.0.0.1:8000/shoppinglist/${id}/edit/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(shoppingList)
        })
    }

    let deleteShoppingList = async () => {
        await fetch(`http://127.0.0.1:8000/shoppinglist/${id}/delete/`,{
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        navigate('/')
    }

    let createShoppingList = async () => {
        await fetch(`http://127.0.0.1:8000/shoppinglist/create-update/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({...shoppingList, 'updated': new Date() })
        })
    }

    let handleSubmit = () => {
        if (id === 'new') {
            createShoppingList();
        } else if (shoppingList.name.trim() === '') { // assuming you want to delete the list if name is empty
            deleteShoppingList();
        } else {
            updateShoppingList();
        }
        navigate('/');
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
                
                setshoppingList(prevState => ({ ...prevState, items: updatedItems }));
            
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
            // Update the shoppingList state to reflect the changes
            const updatedItems = shoppingList.items.map(i => 
                i.id === item.id ? updatedItem : i
            ).sort((a, b) => a.completed - b.completed);
            
    
            setshoppingList(prevState => ({ ...prevState, items: updatedItems }));
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
    
            {id !== 'new' && <button>Add item</button>}
    
            <div className='items-list'>
                {shoppingList?.items && shoppingList.items.map(item => (
                    <div key={item.id} className={`item ${item.completed ? 'completed' : ''}`} onClick={() => handleItemClick(item.id)}>
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
                                onChange={() => handleCompletionChange(item)} 
                            />
                        </div>
                        <div>
                            {item.note && <div className='item-note'>{item.note}</div>}
                        </div>
                    </div>
                ))}
            </div>
            {showModal && (
                <div className="modal">
                    <div className="modal-content">
                        {/* Close Button */}
                        <button onClick={() => setShowModal(false)}>Close</button>

                        {/* Fields for editing */}
                        <input 
                            type="text"
                            value={selectedItem?.product}
                            onChange={(e) => setSelectedItem(prev => ({ ...prev, product: e.target.value }))}
                        />
                        <input 
                            type="text"
                            value={selectedItem?.quantity}
                            onChange={(e) => setSelectedItem(prev => ({ ...prev, quantity: e.target.value }))}
                        />
                        <select
                            value={selectedItem?.unit}
                            onChange={(e) => setSelectedItem(prev => ({ ...prev, unit: e.target.value }))}
                        >
                            {units.map(unit => (
                                <option key={unit} value={unit}>
                                    {unit.charAt(0).toUpperCase() + unit.slice(1)}
                                </option>
                            ))}
                        </select>
                        <select
                            value={selectedItem?.category}
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
                            value={selectedItem?.note}
                            onChange={(e) => setSelectedItem(prev => ({ ...prev, note: e.target.value }))}
                        />

                        <button onClick={handleItemUpdate}>Save Changes</button>
                    </div>
                </div>
            )}
        </div>
    )
}

export default ShoppingListPage