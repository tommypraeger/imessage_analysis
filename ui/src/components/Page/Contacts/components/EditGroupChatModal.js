import React, { useState } from 'react';
import Modal from 'react-modal';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import { editGroup } from '../utils';
Modal.setAppElement('#root');

const EditGroupChatModal = ({
  open, setOpen, name, allChatNames, setFetchesInProgress
}) => {
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
        defaultValue={name}
        onChange={(event, newValue) => setNewName(newValue)}
        options={allChatNames}
        renderInput={(params) => <TextField
          {...params}
          className='modal-input'
          label='Group Chat Name (exactly as it appears in Messages)'
          variant='outlined' />}
      />

      <button className='btn' onClick={() => {
        editGroup(newName, oldName, setFetchesInProgress);
        setOpen(false);
      }}>
        Edit Group Chat
      </button>
    </Modal>
  );
};

export default EditGroupChatModal;
