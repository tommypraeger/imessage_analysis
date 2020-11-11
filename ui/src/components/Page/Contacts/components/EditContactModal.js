import React, { useState } from 'react';
import Modal from 'react-modal';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { editContact } from '../utils';
Modal.setAppElement('#root');

const EditContactModal = ({ open, setOpen, name, number, allPhoneNumbers }) => {
  const oldName = name;
  const [newName, setNewName] = useState(name);
  const [newNumber, setNewNumber] = useState(number);

  return (
    <Modal
      isOpen={open}
      onRequestClose={() => setOpen(false)}
      className='modal'
      overlayClassName='modal-background'
      shouldFocusAfterRender={false}
    >
      <h2>Edit Contact</h2>

      <TextField
        value={newName}
        onChange={(event, newValue) => setNewName(newValue)}
        className='input'
        label='Name'
        variant='outlined'
      />
      <Autocomplete
        value={newNumber}
        onChange={(event, newValue) => setNewNumber(newValue)}
        options={allPhoneNumbers}
        renderInput={(params) => <TextField
          {...params}
          label='Phone Number'
          variant='outlined'
        />}
      />

      <button onClick={() => editContact(name, number, oldName)}>
        Edit Contact
      </button>
    </Modal>
  );
};

export default EditContactModal;
