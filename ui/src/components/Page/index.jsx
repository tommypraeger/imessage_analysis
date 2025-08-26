import React, { useState, useEffect } from "react";
import "react-datepicker/dist/react-datepicker.css";
import AnalysisPage from "./Analysis";
import ContactsPage from "./Contacts";
import { getFetch } from "./utils";

const Page = ({ page }) => {
  const [contacts, setContacts] = useState({});
  const [fetchesInProgress, setFetchesInProgress] = useState(0);
  // Meaningless variable changed to update contacts
  const [updateContacts, setUpdateContacts] = useState(0);

  useEffect(() => {
    getFetch("get_user_data", setFetchesInProgress)
      .then((userData) => setContacts(userData.contacts))
      .catch((err) => console.log(err))
      .finally(() => setFetchesInProgress((fetches) => fetches - 1));
  }, [setContacts, updateContacts]);
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
        />
      );

    default:
      // Should never be the case
      return <React.Fragment />;
  }
};

export default Page;
