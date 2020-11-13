import React, { useState } from 'react';
import Modal from 'react-modal';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { editGroup } from '../utils';
Modal.setAppElement('#root');

const EditGroupChatModal = ({ open, setOpen, name, allChatNames }) => {
  const oldName = name;
  const [newName, setNewName] = useState(name);

  return (
    <Modal
      isOpen={open}
      onRequestClose={() => {
        setOpen(false);
        setNewName('');
      }}
      className='modal'
      overlayClassName='modal-background'
      shouldFocusAfterRender={false}
    >
      <h2>Edit Group Chat</h2>

      <Autocomplete
        onChange={(event, newValue) => setNewName(newValue)}
        options={allChatNames}
        renderInput={(params) => <TextField
          {...params}
          className='input'
          label='Group Chat Name (exactly as it appears in Messages)'
          variant='outlined' />}
      />

      <button onClick={() => {
        editGroup(newName, oldName);
        setOpen(false);
      }}>
        Edit Contact
      </button>
    </Modal>
  );
};

export default EditGroupChatModal;
