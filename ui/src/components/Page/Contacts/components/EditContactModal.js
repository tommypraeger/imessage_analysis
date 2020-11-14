import React, { useState } from 'react';
import Modal from 'react-modal';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { editContact, phoneNumberFilterOptions } from '../utils';
Modal.setAppElement('#root');

const EditContactModal = ({
  open, setOpen, name, number, allPhoneNumbers, setFetchesInProgress
}) => {
  const oldName = name;
  const [newName, setNewName] = useState(name);
  const [newNumber, setNewNumber] = useState(number);

  return (
    <Modal
      isOpen={open}
      onRequestClose={() => {
        setOpen(false);
        setNewName('');
        setNewNumber('');
      }}
      className='modal'
      overlayClassName='modal-background'
      shouldFocusAfterRender={false}
    >
      <h2>Edit Contact</h2>

      <TextField
        onChange={(event) => setNewName(event.target.value)}
        className='input'
        label='Name'
        variant='outlined'
      />

      <Autocomplete
        onChange={(event, newValue) => setNewNumber(newValue.number)}
        options={allPhoneNumbers}
        getOptionLabel={number => number.formatted}
        filterOptions={phoneNumberFilterOptions}
        renderInput={(params) => <TextField
          {...params}
          className='input'
          label='Phone Number'
          variant='outlined'
        />}
      />

      <button className='btn' onClick={() => {
        editContact(newName, newNumber, oldName, setFetchesInProgress);
        setOpen(false);
      }}>
        Edit Contact
      </button>
    </Modal>
  );
};

export default EditContactModal;
