import { useState } from "react";
import Modal from "components/common/Modal";
import { TextField, Autocomplete } from "@mui/material";
import { addContact, phoneNumberFilterOptions } from "../utils";

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
      className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white w-[min(90vw,640px)] max-h-[90vh] overflow-auto border border-slate-200 rounded-lg p-4 shadow-lg z-50"
      overlayClassName="fixed inset-0 bg-black/40 z-40"
      shouldFocusAfterRender={false}
    >
      <div className="space-y-6">
        <h2 className="text-lg font-semibold">Add Contact</h2>

        <TextField
          onChange={(event) => setName(event.target.value)}
          label="Name"
          variant="outlined"
          margin="normal"
          fullWidth
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
            <TextField {...params} label="Phone Number" variant="outlined" margin="normal" fullWidth />
          )}
        />

        <div className="pt-1">
          <button
            className="inline-flex items-center px-4 py-2 rounded bg-slate-900 text-white disabled:bg-slate-300"
            disabled={!name || !number}
            onClick={() => {
              addContact(name, number, setFetchesInProgress, setUpdateContacts);
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

export default AddContactModal;
