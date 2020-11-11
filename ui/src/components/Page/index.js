import React, { useState, useEffect } from 'react';

import AnalysisPage from './Analysis';
import ContactsPage from './Contacts';

const Page = ({ page }) => {
  const [contacts, setContacts] = useState({});
  const [selectedContact, setSelectedContact] = useState({});
  const [allChatNames, setAllChatNames] = useState([]);
  const [allPhoneNumbers, setAllPhoneNumbers] = useState([]);

  // Something to change to trigger fetching contacts again
  const [refetchContacts, setRefetchContacts] = useState(0);

  useEffect(() => {
    fetch('user_data.json')
      .then(response => response.json())
      .then(userData => setContacts(userData.contacts))
      .catch(err => console.log(err));
  }, [refetchContacts])

  useEffect(() => {
    fetch('http://localhost:5000/api/v1/get_all_chat_names')
      .then(response => response.json())
      .then(chatNames => setAllChatNames(JSON.parse(chatNames)))
      .catch(err => console.log(err));
    fetch('http://localhost:5000/api/v1/get_all_phone_numbers')
      .then(response => response.json())
      .then(phoneNumbers => setAllPhoneNumbers(JSON.parse(phoneNumbers)))
      .catch(err => console.log(err));
  }, [])

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
        <ContactsPage
          contacts={contacts}
          refetchContacts={refetchContacts}
          setRefetchContacts={setRefetchContacts}
          allChatNames={allChatNames}
          allPhoneNumbers={allPhoneNumbers}
        />
      );

    default:
      return (
        <ContactsPage
          contacts={contacts}
          refetchContacts={refetchContacts}
          allChatNames={allChatNames}
          allPhoneNumbers={allPhoneNumbers}
        />
      );
  }
}

export default Page;
