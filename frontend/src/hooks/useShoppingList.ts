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
  (shoppingList: ShoppingList | NewShoppingList) => Promise<void>,
  () => Promise<void>
];

const useShoppingList = (shoppingListId : string | number | undefined): UseShoppingListReturnType => {
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
      if (shoppingListId  && shoppingListId  !== 'new') {  // Added id check here
        const data = await fetchShoppingList(shoppingListId );
        if (data.items) {
          data.items = Array.isArray(data.items) ? sortItems(data.items) : sortItems([data.items]);
        }
        // If description is missing, set a default value or leave it out
        (data as ShoppingList).description = (data as ShoppingList).description || '';
        setShoppingList(data);
      }
    };
  
    fetchData();
  }, [shoppingListId ]);

  const updateShoppingListState = (updatedFields: Partial<ShoppingList | NewShoppingList>) => {
    setShoppingList(prevState => {
      const updatedList: ShoppingList | NewShoppingList = { ...prevState, ...updatedFields };
  
      if ('items' in updatedList && Array.isArray(updatedList.items)) {
        updatedList.items = sortItems(updatedList.items);
      }
  
      return updatedList;
    });
  };

  const saveShoppingList = async (shoppingList: ShoppingList | NewShoppingList) => {
    let response: Response;
    if (shoppingListId  === 'new') {
      response = await createShoppingList(shoppingList as NewShoppingList);
  } else if (shoppingListId ) {
      response = await updateShoppingList(shoppingListId , shoppingList as ShoppingList);
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
    if (shoppingListId  && shoppingListId  !== 'new') {
      const response: Response = await deleteShoppingList(shoppingListId );
      if (response.ok) {
        navigate('/');
      }
    }
  };

  return [shoppingList, updateShoppingListState, saveShoppingList, removeShoppingList];
}

export default useShoppingList;