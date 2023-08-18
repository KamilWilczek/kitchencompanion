import React from 'react'
import { Link } from 'react-router-dom'

let getDate = (shoppingList) => {
  return new Date(shoppingList.updated).toLocaleDateString()
}

let getTitle = (shoppingList) => {
  const title = shoppingList.body.split('\n')[0]

  if (title.length > 45) {
    return title.slice(0, 45)
  }

  return title
}

let getContent = (shoppingList) => {
  let title = getTitle(shoppingList)
  let content = shoppingList.body.replaceAll('\n', ' ')
  content = content.replaceAll(title, "")

  if(content.length > 45) {
    return content.slice(0, 45)
  } else {
    return content
  }
}

const ListItem = ({shoppingList}) => {
  return (
    <Link to={`/note/${shoppingList.id}`}>
      <div className='notes-list-item'>
        <h3>{getTitle(shoppingList)}</h3>
        <p><span>{getDate(shoppingList)}</span>{getContent(shoppingList)}</p>
      </div>
    </Link>
  )
}

export default ListItem