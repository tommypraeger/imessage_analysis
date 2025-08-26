import { useState, useEffect } from "react";
import { Oval } from "react-loader-spinner";
import AddContactModal from "./components/AddContactModal";
import AddGroupChatModal from "./components/AddGroupChatModal";
import Contact from "./components/Contact";
import { getFetch, formatNumbers } from "../utils";

const ContactsPage = ({ contacts, fetchesInProgress, setFetchesInProgress, setUpdateContacts }) => {
  const [addContactModalOpen, setAddContactModalOpen] = useState(false);
  const [addGroupChatModalOpen, setAddGroupChatModalOpen] = useState(false);
  const [allChatNames, setAllChatNames] = useState([]);
  const [allPhoneNumbers, setAllPhoneNumbers] = useState([]);

  useEffect(() => {
    getFetch("get_all_chat_names", setFetchesInProgress)
      .then((chatNames) => setAllChatNames(JSON.parse(chatNames)))
      .catch((err) => console.log(err))
      .finally(() => setFetchesInProgress((fetches) => fetches - 1));

    getFetch("get_all_phone_numbers", setFetchesInProgress)
      .then((phoneNumbers) => setAllPhoneNumbers(formatNumbers(JSON.parse(phoneNumbers))))
      .catch((err) => console.log(err))
      .finally(() => setFetchesInProgress((fetches) => fetches - 1));
  }, [setFetchesInProgress]);

  if (fetchesInProgress > 0) {
    return (
      <div className="loading-gif">
        <Oval color="#1982fc" height={200} width={200} />
      </div>
    );
  }

  return (
    <div className="page">
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
      <div>
        <div className="contacts-section-header">
          <h3>Group Chats</h3>
          <p onClick={() => setAddGroupChatModalOpen(true)}>&#x2795; Add Group Chat</p>
        </div>
        <ul className="contact-list">
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
        <div className="contacts-section-header">
          <h3>Contacts</h3>
          <p onClick={() => setAddContactModalOpen(true)}>&#x2795; Add Contact</p>
        </div>
        <ul className="contact-list">
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
