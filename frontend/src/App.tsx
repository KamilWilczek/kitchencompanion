import './App.css';
import { FC } from 'react';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import ShoppingListsListPage from './pages/ShoppingListsListPage';
import ShoppingListPage from './pages/ShoppingListPage';

const App: FC = () => {
  return (
    <Router>
        <div className="container dark">
          <div className='app'>
            <Header/>
            <Routes>
              <Route path='/' element={<ShoppingListsListPage/>}/>
              <Route path='shoppinglist/:id/edit/' element={<ShoppingListPage/>}/>
            </Routes>
          </div>
        </div>
    </Router>
  );
}

export default App;