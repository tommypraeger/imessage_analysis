import React, { useState, useEffect } from 'react';
import 'react-loader-spinner/dist/loader/css/react-spinner-loader.css';
import AnalysisPage from './Analysis';
import ContactsPage from './Contacts';

const Page = ({ page }) => {
  const [contacts, setContacts] = useState({});
  const [selectedContact, setSelectedContact] = useState({});

  useEffect(() => {
    fetch('user_data.json')
      .then(response => response.json())
      .then(userData => setContacts(userData.contacts))
      .catch(err => console.log(err));
  }, []);

  switch (page) {
    case 'analysis':
      return (
        <AnalysisPage
          contacts={contacts}
          selectedContact={selectedContact}
          setSelectedContact={setSelectedContact}
        />
      );

    case 'contacts':
      return (
        <ContactsPage contacts={contacts} />
      );

    default:
      // page currently defaults to 'contacts' so this logic is not really needed
      if (Object.values(contacts).length === 0) {
        return (
          <ContactsPage contacts={contacts} />
        );
      }
      return (
        <AnalysisPage
          contacts={contacts}
          selectedContact={selectedContact}
          setSelectedContact={setSelectedContact}
        />
      );
  }
}

export default Page;
