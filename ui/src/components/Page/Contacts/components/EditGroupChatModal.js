import React, { useState } from "react";
import Modal from "react-modal";
import { TextField, Autocomplete } from "@mui/material";
import { editGroup } from "../utils";
Modal.setAppElement("#root");

const EditGroupChatModal = ({
  open,
  setOpen,
  name,
  allChatNames,
  setFetchesInProgress,
  setUpdateContacts,
}) => {
  const oldName = name;
  const [newName, setNewName] = useState(name);

  return (
    <Modal
      isOpen={open}
      onRequestClose={() => {
        setOpen(false);
        setNewName("");
      }}
      className="modal"
      overlayClassName="modal-background"
      shouldFocusAfterRender={false}
    >
      <h2>Edit Group Chat</h2>

      <Autocomplete
        defaultValue={name}
        onChange={(event, newValue) => setNewName(newValue)}
        options={allChatNames}
        renderInput={(params) => (
          <TextField
            {...params}
            className="modal-input"
            label="Group Chat Name (exactly as it appears in Messages)"
            variant="outlined"
          />
        )}
      />

      <button
        className="btn"
        disabled={!newName}
        onClick={() => {
          editGroup(newName, oldName, setFetchesInProgress, setUpdateContacts);
          setOpen(false);
        }}
      >
        Edit Group Chat
      </button>
    </Modal>
  );
};

export default EditGroupChatModal;
