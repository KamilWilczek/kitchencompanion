import React, {useState, useEffect} from 'react'
import ListItem from '../components/ListItem'
import AddButton from '../components/AddButton'

const ShoppingListsListPage = () => {

    let [shoppingLists, setShoppingLists] = useState([])

    useEffect(() => {
        getShoppingLists()
    }, [])

    let getShoppingLists = async () => {
        let response = await fetch('http://127.0.0.1:8000/shoppinglist/')
        let data = await response.json()
        console.log('DATA:', data)
        setShoppingLists(data)
    }

  return (
    <div className='shoppinglists'>
        <div className='shoppinglists-header'>
            <h2 className='shoppinglists-title'>&#9782; Shopping Lists</h2>
            <p className='shoppinglists-count'>{shoppingLists.length}</p>
        </div>
        <div className='shoppinglists-list'>
            {shoppingLists.map((shoppingList, index) => (
                <ListItem key={index} shoppingList={shoppingList} />
            ))}
        </div>
        <AddButton />
    </div>

  )
}

export default ShoppingListsListPage