import React, { useState } from "react";
import Modal from "react-modal";
import { TextField, Autocomplete } from "@mui/material";
import { addContact, phoneNumberFilterOptions } from "../utils";
Modal.setAppElement("#root");

const AddContactModal = ({
  open,
  setOpen,
  allPhoneNumbers,
  setFetchesInProgress,
  setUpdateContacts,
}) => {
  const [name, setName] = useState("");
  const [number, setNumber] = useState("");

  return (
    <Modal
      isOpen={open}
      onRequestClose={() => {
        setOpen(false);
        setName("");
        setNumber("");
      }}
      className="modal"
      overlayClassName="modal-background"
      shouldFocusAfterRender={false}
    >
      <h2>Add Contact</h2>

      <TextField
        onChange={(event) => setName(event.target.value)}
        className="modal-input"
        label="Name"
        variant="outlined"
      />

      <Autocomplete
        onChange={(event, newValue) => {
          if (newValue) {
            setNumber(newValue.number);
          } else {
            setNumber("");
          }
        }}
        options={allPhoneNumbers}
        filterOptions={phoneNumberFilterOptions}
        getOptionLabel={(number) => number.formatted}
        renderInput={(params) => (
          <TextField {...params} className="modal-input" label="Phone Number" variant="outlined" />
        )}
      />

      <button
        className="btn"
        disabled={!name || !number}
        onClick={() => {
          addContact(name, number, setFetchesInProgress, setUpdateContacts);
          setOpen(false);
        }}
      >
        Add Contact
      </button>
    </Modal>
  );
};

export default AddContactModal;
