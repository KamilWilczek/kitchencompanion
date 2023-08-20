import React from 'react'
import { Link } from 'react-router-dom'

let getDate = (shoppingList) => {
  return new Date(shoppingList.updated).toLocaleDateString()
}

let getName = (shoppingList) => {
  const name = shoppingList.name

  return name
}


const ListItem = ({shoppingList}) => {
  return (
    <Link to={`shoppinglist/${shoppingList.id}/edit/`}>
      <div className='shoppinglists-list-item'>
        <h3>{getName(shoppingList)}</h3>
        <p><span>{getDate(shoppingList)}</span></p>
        <p>Items count: {shoppingList.items_count}</p>
      </div>
    </Link>
  )
}

export default ListItem