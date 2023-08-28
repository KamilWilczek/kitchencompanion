## kitchencompanion

# TODO

## Architecture

- [x] ShoppingList module
- [ ] Recipe module
- [ ] Pantry module
- [ ] Planner module
- [x] JS to TS port
- [ ] Database: PostgreSQL
- [ ] Look for better layout
- [ ] Bootstrap?
  - [ ] React MUI
  - [ ] Figma
  - [ ] Canva
- [ ] Add user creation UsersApp
  - [ ] some plugins for user creation in Django
- [ ] Authentication
- [ ] dependencies management
  - [ ] poetry

## Backend

- [ ] ShoppingList module
  - [x] Models for ShoppingList
  - [x] Basic CRUD for ShoppingList
  - [x] Basic CRUD for ShoppingListItem
  - [ ] ...
- [x] Typing
- [ ] Refactor views.py
  - [x] Class based views
  - [ ] Exception Handling in ShoppingItemMixin
- [ ] Field validation
- [ ] Linting
  - [ ] pylint
  - [ ] isort
- [ ] Tests
  - [ ] Unit tests
  - [ ] Integration tests

## Frontend

- [ ] ShoppingList module

  - [ ] ShoppingList
    - [x] Retrieve itemShoppingLists
    - [x] Edit ShoppingList
    - [x] Add ShoppingList
    - [x] Extract Item, Itemslist, ItemModal as components
    - [x] Remove ShoppingList
    - [ ] Remove bought items
    - [ ] Remove all items
    - [ ] Refactoring:
      - [x] Modularize components (e.g., `ShoppingListHeader`, `ShoppingListInputs`)
      - [ ] Implement `useCallback` for event handlers
      - [ ] Consolidate state management (consider `Redux`,`Zustand`, and `MobX`)
      - [ ] Improve error handling for async operations
      - [x] Ensure consistent function naming
      - [ ] Add comments for complex logic
      - [ ] Avoid direct arrow functions in JSX for performance
    - [ ] ...
  - [ ] Items
    - [x] Retrieve items
      - [x] Sorting
    - [x] Edit Item
      - [x] Modal
      - [x] completion on checkbox
    - [x] Add item
      - [x] Modal
      - [ ] while typing name gives hints or gives previously used
    - [x] Remove item
      - [x] removal on Modal
      - [ ] side banner for returning delete action
    - [ ] Refactoring:
      - [ ] Move item-related logic to a separate custom hook (e.g., `useShoppingListItem`)
      - [ ] Modularize components related to individual items
      - [ ] Implement `useCallback` for item-related event handlers
      - [ ] Improve error handling for async item operations
      - [ ] Ensure consistent function naming for item-related functions
      - [ ] Add comments for complex item-related logic
      - [ ] Avoid direct arrow functions in JSX for item components for performance
      - [ ] Destructure state and props at the beginning of item-related components for readability
    - [ ] ...

- [ ] Field validation
- [ ] somethin with fetches, don't like them
  - [x] extract basic CRUD for ShoppingListPage.js
  - [x] move apiUtils.js into better place
  - [x] ShoppingList frontend api in one place
  - [ ] axios?
- [ ] Lint

  - [ ] prettier
  - [ ] ESLint

## Utility

- [ ] Better README
