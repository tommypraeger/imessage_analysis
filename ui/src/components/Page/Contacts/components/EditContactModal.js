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
        defaultValue={name}
        onChange={(event) => setNewName(event.target.value)}
        className='modal-input'
        label='Name'
        variant='outlined'
      />

      <Autocomplete
        defaultValue={allPhoneNumbers.filter(numObj => numObj.number === number)[0]}
        onChange={(event, newValue) => {
          if (newValue) {
            setNewNumber(newValue.number);
          } else {
            setNewNumber('');
          }
        }}
        options={allPhoneNumbers}
        getOptionLabel={numberObj => numberObj.formatted}
        filterOptions={phoneNumberFilterOptions}
        renderInput={(params) => <TextField
          {...params}
          className='modal-input'
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
