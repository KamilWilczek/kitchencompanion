# ShoppingListView:

- [x] Test if all shopping lists are returned.
- [x] Test if the items_count annotation returns the correct number of items for each shopping list.

# ShoppingListCreateView:

- [x] Test creating a new shopping list.
- [x] Test creating a shopping list with invalid data (missing required fields, invalid data types, etc.).

# ShoppingListDetailUpdateView:

- [x] Test retrieving a specific shopping list by ID.
- [x] Test updating a specific shopping list by ID.
- [x] Test updating a shopping list with invalid data.
- [x] Test trying to retrieve a non-existent shopping list (expect a 404 status).

# ShoppingListDeleteView:

- [x] Test deleting a specific shopping list by ID.
- [x] Test trying to delete a non-existent shopping list.

# ItemUpdateView:

- [x] Test retrieving a specific item by ID from a specific shopping list.
- [x] Test updating a specific item by ID from a shopping list.
- [x] Test updating an item with invalid data.
- [x] Test trying to retrieve a non-existent item from a shopping list.

# ItemCreateView:

- [x] Test adding a new item to a specific shopping list.
- [x] Test trying to add an item with invalid data to a shopping list.
- [x] Test trying to add an item to a non-existent shopping list.

# ItemDeleteView:

- [x] Test deleting a specific item by ID from a specific shopping list.
- [x] Test trying to delete a non-existent item from a shopping list.

# Additional Cases for All Views:

- [x] Test response format (to make sure it's returning the expected format for both success and error scenarios).
- [ ] Ensure that unauthorized users can't create a shopping list. Similarly, test whether users can create lists for other users.
- [x] If creating a shopping list with the same data multiple times should lead to unique entries each time, ensure that this is the case. On the other hand, if it shouldn't, then ensure that subsequent POSTs with the same data don't create duplicates.
