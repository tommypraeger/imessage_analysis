import React, { useState, useEffect } from "react";
import AnalysisPage from "./Analysis";
import ContactsPage from "./Contacts";
import { getFetch, formatNumbers } from "./utils";

const Page = ({ page }) => {
  const [contacts, setContacts] = useState({});
  const [fetchesInProgress, setFetchesInProgress] = useState(0);
  // Meaningless variable changed to update contacts
  const [updateContacts, setUpdateContacts] = useState(0);
  const [allChatNames, setAllChatNames] = useState([]);
  const [allPhoneNumbers, setAllPhoneNumbers] = useState([]);

  useEffect(() => {
    getFetch("get_user_data", setFetchesInProgress)
      .then((userData) => setContacts(userData.contacts))
      .catch((err) => console.log(err))
      .finally(() => setFetchesInProgress((fetches) => fetches - 1));
  }, [setContacts, updateContacts]);

  // Fetch shared ancillary data once and cache in parent
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
  switch (page) {
    case "analysis":
      return (
        <AnalysisPage
          contacts={contacts}
          fetchesInProgress={fetchesInProgress}
          setFetchesInProgress={setFetchesInProgress}
        />
      );

    case "contacts":
      return (
        <ContactsPage
          contacts={contacts}
          fetchesInProgress={fetchesInProgress}
          setFetchesInProgress={setFetchesInProgress}
          setUpdateContacts={setUpdateContacts}
          allChatNames={allChatNames}
          allPhoneNumbers={allPhoneNumbers}
        />
      );

    default:
      // Should never be the case
      return <React.Fragment />;
  }
};

export default Page;
