import React, { useState } from 'react';
import Modal from 'react-modal';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { addGroup } from '../utils';
Modal.setAppElement('#root');

const AddGroupChatModal = ({ open, setOpen, allChatNames }) => {
  const [name, setName] = useState('');

  return (
    <Modal
      isOpen={open}
      onRequestClose={() => setOpen(false)}
      className='modal'
      overlayClassName='modal-background'
      shouldFocusAfterRender={false}
    >
      <h2>Add Group Chat</h2>

      <Autocomplete
        value={name}
        onChange={(event, newValue) => setName(newValue)}
        options={allChatNames}
        renderInput={(params) => <TextField
          {...params}
          className='input'
          label='Group Chat Name (exactly as it appears in Messages)'
          variant='outlined' />}
      />

      <button onClick={() => addGroup(name)}>
        addContact
    </button>
    </Modal>
  );
};

export default AddGroupChatModal;
