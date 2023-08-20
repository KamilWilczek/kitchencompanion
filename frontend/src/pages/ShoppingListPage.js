import React, { useState, useEffect }  from 'react'
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import { ReactComponent as ArrowLeft } from '../assets/arrow-left.svg'

const ShoppingListPage = () => {
    let {id} = useParams();
    let [shoppingList, setshoppingList] = useState(null)
    const navigate = useNavigate();

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

    return (
        <div className='shoppinglist'>
            <div className='shoppinglist-header'>
                <h3>
                    <ArrowLeft onClick={handleSubmit}/>
                </h3>
                {id !== 'new' ? (<button onClick={deleteShoppingList}>Delete</button>) : (<button onClick={handleSubmit}>Done</button>)} 
            </div>
            {/* Input for 'name' */}
            <input 
                type="text"
                placeholder="Shopping List Name"
                onChange={(e) => handleChange('name', e.target.value)} 
                value={shoppingList?.name}
            />
    
            {/* Input for 'description' */}
            <input 
                type="text"
                placeholder="Description"
                onChange={(e) => handleChange('description', e.target.value)} 
                value={shoppingList?.description}
            />
            {id !== 'new' && <button>Add item</button>}

            <div className='items-list'>
                {shoppingList?.items && shoppingList.items.map(item => (
                    <div key={item.id} className='item'>
                        <div className='item-name'>{item.product}</div>
                        {item.quantity && <div className='item-quantity'>{item.quantity}</div>}
                        {item.unit && <div className='item-unit'>{item.unit}</div>}
                        {item.note && <div className='item-note'>{item.note}</div>}
                        <div className='item-category'>{item.category}</div>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default ShoppingListPage