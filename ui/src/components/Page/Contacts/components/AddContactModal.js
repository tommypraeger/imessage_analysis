import React, { useState } from 'react';
import Modal from 'react-modal';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { addContact } from '../utils';
Modal.setAppElement('#root');

const AddContactModal = ({ open, setOpen, allPhoneNumbers }) => {
  const [name, setName] = useState('');
  const [number, setNumber] = useState('');
  console.log(name);

  return (
    <Modal
      isOpen={open}
      onRequestClose={() => setOpen(false)}
      className='modal'
      overlayClassName='modal-background'
      shouldFocusAfterRender={false}
    >
      <h2>Add Contact</h2>

      <TextField
        value={name}
        onChange={(event) => setName(event.target.value)}
        className='input'
        label='Name'
        variant='outlined'
      />
      <Autocomplete
        value={number}
        onChange={(event, newValue) => setNumber(newValue)}
        options={allPhoneNumbers}
        renderInput={(params) => <TextField
          {...params}
          label='Phone Number'
          variant='outlined'
        />}
      />

      <button onClick={() => addContact(name, number)}>
        Add Contact
      </button>
    </Modal>
  );
};

export default AddContactModal;
