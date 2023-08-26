import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchShoppingList, updateShoppingList, createShoppingList, deleteShoppingList } from '../utils/apiUtils';
import { ShoppingList, NewShoppingList, ShoppingListItem } from '../utils/types';


interface Response {
  ok: boolean;
  [key: string]: any;  // Add additional properties as needed based on the structure of your response
}

type UseShoppingListReturnType = [
  ShoppingList | NewShoppingList,
  (updatedFields: Partial<ShoppingList | NewShoppingList>) => void,
  (list: ShoppingList | NewShoppingList) => Promise<void>,
  () => Promise<void>
];

const useShoppingList = (id: string | number | undefined): UseShoppingListReturnType => {
  const navigate = useNavigate();
  const [shoppingList, setShoppingList] = useState<ShoppingList | NewShoppingList>({ name: "", description: "", items: [] });

  const sortItems = (items: ShoppingListItem[]): ShoppingListItem[] => {
    return items.sort((a, b) => {
      if (a.completed !== b.completed) return a.completed ? 1 : -1;

      if (a.product.toLowerCase() < b.product.toLowerCase()) return -1;
      if (a.product.toLowerCase() > b.product.toLowerCase()) return 1;
      return 0;
    });
  };

  useEffect(() => {
    const fetchData = async () => {
      if (id && id !== 'new') {  // Added id check here
        const data = await fetchShoppingList(id);
        if (data.items) {
          data.items = Array.isArray(data.items) ? sortItems(data.items) : sortItems([data.items]);
        }
        // If description is missing, set a default value or leave it out
        (data as ShoppingList).description = (data as ShoppingList).description || '';
        setShoppingList(data);
      }
    };
  
    fetchData();
  }, [id]);

  const updateShoppingListState = (updatedFields: Partial<ShoppingList | NewShoppingList>) => {
    setShoppingList(prevState => {
      const updatedList: ShoppingList | NewShoppingList = { ...prevState, ...updatedFields };
  
      if ('items' in updatedList && Array.isArray(updatedList.items)) {
        updatedList.items = sortItems(updatedList.items);
      }
  
      return updatedList;
    });
  };

  const saveShoppingList = async (list: ShoppingList | NewShoppingList) => {
    let response: Response;
    if (id === 'new') {
      response = await createShoppingList(list as NewShoppingList);
  } else if (id) {
      response = await updateShoppingList(id, list as ShoppingList);
  } else {
      return;
  }

    if (response.ok) {
      navigate('/');
    } else {
      console.error('Failed response:', response);
    }
  };

  const removeShoppingList = async () => {
    if (id && id !== 'new') {
      const response: Response = await deleteShoppingList(id);
      if (response.ok) {
        navigate('/');
      }
    }
  };

  return [shoppingList, updateShoppingListState, saveShoppingList, removeShoppingList];
}

export default useShoppingList;