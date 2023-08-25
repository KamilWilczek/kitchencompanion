import React, { FC } from 'react';
import { Link } from 'react-router-dom';
import { ReactComponent as AddIcon } from '../assets/add.svg';

const AddButton: FC = () => {
  return (
    <Link to="shoppinglist/new/edit" className='floating-button'>
        <AddIcon />
    </Link>
  )
}

export default AddButton;