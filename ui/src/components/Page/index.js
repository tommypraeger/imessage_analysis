import React, { useState, useEffect } from 'react';

import AnalysisPage from './Analysis';
import ContactsPage from './Contacts';
import HomePage from './Home';

const Page = ({ page }) => {
  const [contacts, setContacts] = useState({});
  const [selectedContact, setSelectedContact] = useState({});

  useEffect(() => {
    fetch('user_data.json')
      .then(response => response.json())
      .then(userData => setContacts(userData.contacts))
  }, [])

  switch (page) {
    case 'analysis':
      return <AnalysisPage
        contacts={contacts}
        selectedContact={selectedContact}
        setSelectedContact={setSelectedContact}
      />;

    case 'contacts':
      return <ContactsPage
        contacts={contacts}
        selectedContact={selectedContact}
      />;

    case 'home':
      return <HomePage />;

    default:
      return <HomePage />;
  }
}

export default Page;
