import React, { useState, useEffect } from 'react';
import ShoppingList from '../components/ShoppingList';
import AddButton from '../components/AddButton';
import { fetchShoppingLists } from '../utils/apiUtils';
import { ShoppingList as ShoppingListType } from '../utils/types';


const ShoppingListsListPage: React.FC = () => {

    const [shoppingLists, setShoppingLists] = useState<ShoppingListType[]>([]);

    useEffect(() => {
        getShoppingLists();
    }, []);

    const getShoppingLists = async () => {
        const data = await fetchShoppingLists();
        setShoppingLists(data);
    }

    return (
        <div className='shoppinglists'>
            <div className='shoppinglists-header'>
                <h2 className='shoppinglists-title'>&#9782; Shopping Lists</h2>
                <p className='shoppinglists-count'>{shoppingLists.length}</p>
            </div>
            <div className='shoppinglists-list'>
                {shoppingLists.map((shoppingList, index) => (
                    <ShoppingList key={index} shoppingList={shoppingList} />
                ))}
            </div>
            <AddButton />
        </div>
    );
}

export default ShoppingListsListPage;