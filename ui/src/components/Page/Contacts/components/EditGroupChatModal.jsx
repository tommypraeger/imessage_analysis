import { useState } from "react";
import Modal from "components/common/Modal";
import { TextField, Autocomplete } from "@mui/material";
import { editGroup } from "../utils";

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
      className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white w-[min(90vw,640px)] max-h-[90vh] overflow-auto border border-slate-200 rounded-lg p-5 shadow-lg z-50"
      overlayClassName="fixed inset-0 bg-black/40 z-40"
      shouldFocusAfterRender={false}
    >
      <div className="space-y-4">
        <h2 className="text-lg font-semibold">Edit Group Chat</h2>

      <Autocomplete
        defaultValue={name}
        onChange={(event, newValue) => setNewName(newValue)}
        options={allChatNames}
        renderInput={(params) => (
          <TextField
            {...params}
            label="Group Chat Name (exactly as it appears in Messages)"
            variant="outlined"
            fullWidth
          />
        )}
      />

      <div className="pt-1">
        <button
          className="inline-flex items-center px-4 py-2 rounded bg-slate-900 text-white disabled:bg-slate-300"
          disabled={!newName}
          onClick={() => {
            editGroup(newName, oldName, setFetchesInProgress, setUpdateContacts);
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

export default EditGroupChatModal;
