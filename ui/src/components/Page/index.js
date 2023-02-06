import React, { useState, useEffect } from "react";
import "react-datepicker/dist/react-datepicker.css";
import AnalysisPage from "./Analysis";
import ContactsPage from "./Contacts";

const Page = ({ page }) => {
  const [contacts, setContacts] = useState({});

  useEffect(() => {
    fetch("user_data.json")
      .then((response) => response.json())
      .then((userData) => setContacts(userData.contacts))
      .catch((err) => console.log(err));
  }, []);

  switch (page) {
    case "analysis":
      return <AnalysisPage contacts={contacts} />;

    case "contacts":
      return <ContactsPage contacts={contacts} setContacts={setContacts} />;

    default:
      // Should never be the case
      return <React.Fragment />;
  }
};

export default Page;
