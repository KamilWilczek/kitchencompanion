import { useState, useEffect, FC } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchShoppingList, updateShoppingList, createShoppingList, deleteShoppingList } from '../utils_ts/apiUtils';

interface Item {
  product: string;
  completed: boolean;
}

interface ShoppingList {
  name: string;
  description: string;
  items: Item[];
}

interface Response {
  ok: boolean;
  [key: string]: any;  // Add additional properties as needed based on the structure of your response
}

const useShoppingList: FC<string> = (id) => {
  const navigate = useNavigate();
  const [shoppingList, setShoppingList] = useState<ShoppingList>({ name: "", description: "", items: [] });

  const sortItems = (items: Item[]): Item[] => {
    return items.sort((a, b) => {
      if (a.completed !== b.completed) return a.completed ? 1 : -1;

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

  const updateShoppingListState = (updatedFields: Partial<ShoppingList>) => {
    setShoppingList(prevState => {
      const updatedList: ShoppingList = { ...prevState, ...updatedFields };

      if (updatedList.items && Array.isArray(updatedList.items)) {
        updatedList.items = sortItems(updatedList.items);
      }

      return updatedList;
    });
  };

  const saveShoppingList = async (list: ShoppingList) => {
    let response: Response;
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
    let response: Response;
    if (id !== 'new') {
      response = await deleteShoppingList(id);
    }
    if (response.ok) {
      navigate('/');
    } else {
      // Handle the error or display a notification to the user.
    }
  };

  return [shoppingList, updateShoppingListState, saveShoppingList, removeShoppingList];
}

export default useShoppingList;