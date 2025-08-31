import { useState } from "react";
import LoadingSpinner from "components/common/LoadingSpinner";
import AddContactModal from "./components/AddContactModal";
import AddGroupChatModal from "./components/AddGroupChatModal";
import Contact from "./components/Contact";

const ContactsPage = ({ contacts, fetchesInProgress, setFetchesInProgress, setUpdateContacts, allChatNames, allPhoneNumbers }) => {
  const [addContactModalOpen, setAddContactModalOpen] = useState(false);
  const [addGroupChatModalOpen, setAddGroupChatModalOpen] = useState(false);

  if (fetchesInProgress > 0) {
    return (
      <div className="w-[200px] mx-auto mt-16 mb-5 flex items-center justify-center">
        <LoadingSpinner size={64} />
      </div>
    );
  }

  return (
    <div>
      <AddContactModal
        open={addContactModalOpen}
        setOpen={setAddContactModalOpen}
        allPhoneNumbers={allPhoneNumbers}
        setFetchesInProgress={setFetchesInProgress}
        setUpdateContacts={setUpdateContacts}
      />
      <AddGroupChatModal
        open={addGroupChatModalOpen}
        setOpen={setAddGroupChatModalOpen}
        allChatNames={allChatNames}
        setFetchesInProgress={setFetchesInProgress}
        setUpdateContacts={setUpdateContacts}
      />
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold">Group Chats</h3>
          <button className="text-slate-600 hover:text-slate-900" onClick={() => setAddGroupChatModalOpen(true)}>&#x2795; Add Group Chat</button>
        </div>
        <ul className="grid grid-cols-1 md:grid-cols-2 gap-3 list-none p-0">
          {Object.keys(contacts)
            .filter((name) => contacts[name] === "group")
            .map((name) => (
              <Contact
                key={name}
                name={name}
                allChatNames={allChatNames}
                allPhoneNumbers={allPhoneNumbers}
                setFetchesInProgress={setFetchesInProgress}
                setUpdateContacts={setUpdateContacts}
              />
            ))}
        </ul>
      </div>
      <div>
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold">Contacts</h3>
          <button className="text-slate-600 hover:text-slate-900" onClick={() => setAddContactModalOpen(true)}>&#x2795; Add Contact</button>
        </div>
        <ul className="grid grid-cols-1 md:grid-cols-2 gap-3 list-none p-0">
          {Object.keys(contacts)
            .filter((name) => contacts[name] !== "group")
            .map((name) => (
              <Contact
                key={name}
                name={name}
                number={contacts[name]}
                allChatNames={allChatNames}
                allPhoneNumbers={allPhoneNumbers}
                setFetchesInProgress={setFetchesInProgress}
                setUpdateContacts={setUpdateContacts}
              />
            ))}
        </ul>
      </div>
    </div>
  );
};

export default ContactsPage;
