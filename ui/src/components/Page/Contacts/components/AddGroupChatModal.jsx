import { useState } from "react";
import Modal from "react-modal";
import { TextField, Autocomplete } from "@mui/material";
import { addGroup } from "../utils";
if (typeof document !== "undefined" && document.getElementById("root")) {
  Modal.setAppElement("#root");
}

const AddGroupChatModal = ({
  open,
  setOpen,
  allChatNames,
  setFetchesInProgress,
  setUpdateContacts,
}) => {
  const [name, setName] = useState("");

  return (
    <Modal
      isOpen={open}
      onRequestClose={() => {
        setOpen(false);
        setName("");
      }}
      className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white w-[min(90vw,640px)] max-h-[90vh] overflow-auto border border-slate-200 rounded-lg p-4 shadow-lg z-50"
      overlayClassName="fixed inset-0 bg-black/40 z-40"
      shouldFocusAfterRender={false}
    >
      <div className="space-y-6">
        <h2 className="text-lg font-semibold">Add Group Chat</h2>

        <Autocomplete
          onChange={(event, newValue) => setName(newValue)}
          options={allChatNames}
          renderInput={(params) => (
            <TextField
              {...params}
              label="Group Chat Name (exactly as it appears in Messages)"
              variant="outlined"
              margin="normal"
              fullWidth
            />
          )}
        />

        <div className="pt-1">
          <button
            className="inline-flex items-center px-4 py-2 rounded bg-slate-900 text-white disabled:bg-slate-300"
            disabled={!name}
            onClick={() => {
              addGroup(name, setFetchesInProgress, setUpdateContacts);
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

export default AddGroupChatModal;
