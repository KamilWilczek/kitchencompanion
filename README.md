## kitchencompanion

# TODO

## MVP

- shopping list
- accounts
- recipe module

## Architecture

- [x] ShoppingList module
- [ ] Recipe module
  - [ ] Basic CRUD
  - [ ] Recipe versioning on Recipe Page, ex: on Burrito: burrito_1, burrito_2,
  - [ ] Picture in recipe model
  - [ ] Tags: Beef, Vegan, Pasta, Breakfast
    - [ ] Multi-choice
  - [ ] One click to add to shopping list
    - [ ] Modal with list Items List, choose to add
    - [ ] Shows on Recipes which ingredients I already have in my pantry
    - This way we won't end up with 10kg with flour
  - [ ] Solve adding items on shopping list from two recipes
  - [ ] Portions
  - [ ] Time preparing
  - [ ] Ingredients List
    - Ingredients List and Items to buy are different
    - Items to buy are added to Shopping Lists
    - Ingredients List are the ones that are needed for prep recipe
    - Ingredients List olive - 2 tablespoons, how to buy that? How to add spoons to Shopping List? How to buy 12 spoons?
    - This way in one list we habe 2 tablespoon to prep, and on Shopping List we add just olive.
  - [ ] Scrapping recipe from picture
  - [ ] Scraping recipe from web
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
- [ ] Sharing list between accounts
- [ ] Items tracking for charts
- [ ] Category BREAD change to BAKERY
- [ ] Indeks skladikow w przepisie, wyszukiwanie po skladniku, sprawdzanie w jakim przepisie jest fikusny skladnik,
- [ ] Localize to PL
- [ ] Shows on Recipes which ingredients I already have in my pantry

## Backend

- [ ] ShoppingList module
  - [x] Models for ShoppingList
  - [x] Basic CRUD for ShoppingList
  - [x] Basic CRUD for ShoppingListItem
  - [x] Shopping List name validation
    - [x] Do not allow for `'     '`
  - [x] Item product validation
    - [x] Do not allow for `'     '`
  - [ ] ...
- [x] Typing
- [ ] Refactor views.py
  - [x] Class based views
  - [ ] Exception Handling in ShoppingItemMixin
- [ ] Field validation
- [ ] Linting
  - [ ] pylint
  - [x] isort
- [ ] Tests
  - [x] `pytest` and `pytest-django` plugin
  - [ ] Unit tests
    - [x] models.py
    - [x] views.py
    - [ ] serializers.py
    - [ ] mixins.py
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
    - [ ] Ordering: completion, category
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
