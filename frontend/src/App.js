import './App.css';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom"
import Header from './components/Header'
import ShoppingListsListPage from './pages/ShoppingListsListPage'
import ShoppingListPage from './pages/ShoppingListPage';

function App() {
  return (
    <Router>
        <div className="container dark">
          <div className='app'>
            <Header/>
            <Routes>
              <Route path='/' element={<ShoppingListsListPage/>}/>
              <Route path='/shoppinglist/:id' element={<ShoppingListPage/>}/>
            </Routes>
          </div>
        </div>
    </Router>
  );
}

export default App;
