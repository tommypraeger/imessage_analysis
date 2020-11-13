import React, { useState } from 'react';
import Modal from 'react-modal';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { addContact, phoneNumberFilterOptions } from '../utils';
Modal.setAppElement('#root');

const AddContactModal = ({ open, setOpen, allPhoneNumbers }) => {
  const [name, setName] = useState('');
  const [number, setNumber] = useState('');

  return (
    <Modal
      isOpen={open}
      onRequestClose={() => {
        setOpen(false);
        setName('');
        setNumber('');
      }}
      className='modal'
      overlayClassName='modal-background'
      shouldFocusAfterRender={false}
    >
      <h2>Add Contact</h2>

      <TextField
        onChange={(event) => setName(event.target.value)}
        className='input'
        label='Name'
        variant='outlined'
      />

      <Autocomplete
        onChange={(event, newValue) => setNumber(newValue.number)}
        options={allPhoneNumbers}
        filterOptions={phoneNumberFilterOptions}
        getOptionLabel={number => number.formatted}
        renderInput={(params) => <TextField
          {...params}
          className='input'
          label='Phone Number'
          variant='outlined'
        />}
      />

      <button onClick={() => {
        addContact(name, number);
        setOpen(false);
      }}>
        Add Contact
      </button>
    </Modal>
  );
};

export default AddContactModal;
