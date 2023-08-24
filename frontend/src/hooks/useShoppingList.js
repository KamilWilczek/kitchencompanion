import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchShoppingList, updateShoppingList, createShoppingList, deleteShoppingList } from '../utils/apiUtils';

const useShoppingList = (id) => {
    const navigate = useNavigate();
    const [shoppingList, setShoppingList] = useState({ name: "", description: "", items: [] });

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
        const fetchData = async () => {
            if (id !== 'new') {
                const data = await fetchShoppingList(id);
                if (data.items) {
                    data.items = Array.isArray(data.items) ? data.items : [data.items];
                    data.items = sortItems(data.items);
                }
                setShoppingList(data);
            }
        };
        
        fetchData();
    }, [id]);

    const updateShoppingListState = (updatedFields) => {
        setShoppingList(prevState => {
            // First, spread out the previous state and updated fields
            const updatedList = { ...prevState, ...updatedFields };
    
            // If items exist and it's an array, sort them
            if (updatedList.items && Array.isArray(updatedList.items)) {
                updatedList.items = sortItems(updatedList.items);
            }
    
            return updatedList;
        });
    };

    const saveShoppingList = async (list) => {
        let response;
        if (id === 'new') {
            response = await createShoppingList(list);
        } else {
            response = await updateShoppingList(id, list);
        }

        if (response.ok) {
            navigate('/');  // or wherever you want to redirect to
        } else {
            // Handle the error or display a notification to the user.
        }
    };

    const removeShoppingList = async () => {
        let response;
        if (id !== 'new') {
            response = await deleteShoppingList(id);
        }
        if (response.ok) {
            navigate('/');
        } else {

        }
    };

    return [shoppingList, updateShoppingListState, saveShoppingList, removeShoppingList];
}

export default useShoppingList;