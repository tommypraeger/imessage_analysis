import React, { useState } from "react";
import EditContactModal from "./EditContactModal";
import EditGroupChatModal from "./EditGroupChatModal";
import { deleteContact, deleteGroup } from "../utils";
import { formatNumber } from "../../utils";

const Contact = ({
  name,
  number,
  allPhoneNumbers,
  allChatNames,
  setFetchesInProgress,
  setUpdateContacts,
}) => {
  const [editContactModalOpen, setEditContactModalOpen] = useState(false);
  const [editGroupChatModalOpen, setEditGroupChatModalOpen] = useState(false);

  return (
    <React.Fragment>
      <EditContactModal
        open={editContactModalOpen}
        setOpen={setEditContactModalOpen}
        name={name}
        number={number}
        allPhoneNumbers={allPhoneNumbers}
        setFetchesInProgress={setFetchesInProgress}
        setUpdateContacts={setUpdateContacts}
      />
      <EditGroupChatModal
        open={editGroupChatModalOpen}
        setOpen={setEditGroupChatModalOpen}
        name={name}
        allChatNames={allChatNames}
        setFetchesInProgress={setFetchesInProgress}
        setUpdateContacts={setUpdateContacts}
      />
      <li
        className="cursor-pointer rounded border border-slate-200 bg-white hover:border-slate-300 shadow-sm px-4 py-3 flex items-center justify-between"
        onClick={() => {
          if (number) {
            setEditContactModalOpen(true);
          } else {
            setEditGroupChatModalOpen(true);
          }
        }}
      >
        <div className="flex items-baseline gap-3">
          <p className="font-medium text-slate-900">{name}</p>
          {number ? <p className="text-slate-500">{formatNumber(number)}</p> : ""}
        </div>
        <button
          className="text-slate-400 hover:text-slate-600"
          onClick={(e) => {
            e.stopPropagation();
            if (number) {
              deleteContact(name, setFetchesInProgress, setUpdateContacts);
            } else {
              deleteGroup(name, setFetchesInProgress, setUpdateContacts);
            }
          }}
        >
          &#x2715;
        </button>
      </li>
    </React.Fragment>
  );
};

export default Contact;
