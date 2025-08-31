import { useState } from "react";
import Modal from "components/common/Modal";
import { TextField, Autocomplete } from "@mui/material";
import { editContact, phoneNumberFilterOptions } from "../utils";

const EditContactModal = ({
  open,
  setOpen,
  name,
  number,
  allPhoneNumbers,
  setFetchesInProgress,
  setUpdateContacts,
}) => {
  const oldName = name;
  const [newName, setNewName] = useState(name);
  const [newNumber, setNewNumber] = useState(number);

  return (
    <Modal
      isOpen={open}
      onRequestClose={() => {
        setOpen(false);
        setNewName("");
        setNewNumber("");
      }}
      className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white w-[min(90vw,640px)] max-h-[90vh] overflow-auto border border-slate-200 rounded-lg p-6 shadow-lg z-50"
      overlayClassName="fixed inset-0 bg-black/40 z-40"
      shouldFocusAfterRender={false}
    >
      <div className="space-y-6">
        <h2 className="text-lg font-semibold">Edit Contact</h2>

        <TextField
          defaultValue={name}
          onChange={(event) => setNewName(event.target.value)}
          label="Name"
          variant="outlined"
          margin="normal"
          fullWidth
        />

        <Autocomplete
          defaultValue={allPhoneNumbers.filter((numObj) => numObj.number === number)[0]}
          onChange={(event, newValue) => {
            if (newValue) {
              setNewNumber(newValue.number);
            } else {
              setNewNumber("");
            }
          }}
          options={allPhoneNumbers}
          getOptionLabel={(numberObj) => numberObj.formatted}
          filterOptions={phoneNumberFilterOptions}
          renderInput={(params) => (
            <TextField {...params} label="Phone Number" variant="outlined" margin="normal" fullWidth />
          )}
        />

        <div className="pt-1">
          <button
            className="inline-flex items-center px-4 py-2 rounded bg-slate-900 text-white disabled:bg-slate-300"
            disabled={!newName || !newNumber}
            onClick={() => {
              editContact(newName, newNumber, oldName, setFetchesInProgress, setUpdateContacts);
              setOpen(false);
            }}
          >
            Save
          </button>
        </div>
      </div>
    </Modal>
  );
};

export default EditContactModal;
