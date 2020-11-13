import React, { useState, useEffect } from 'react';
import 'react-loader-spinner/dist/loader/css/react-spinner-loader.css';
import Loader from 'react-loader-spinner';
import AnalysisPage from './Analysis';
import ContactsPage from './Contacts';
import { getFetch, formatNumbers } from './utils';

const Page = ({ page }) => {
  const [contacts, setContacts] = useState({});
  const [selectedContact, setSelectedContact] = useState({});
  const [allChatNames, setAllChatNames] = useState([]);
  const [allPhoneNumbers, setAllPhoneNumbers] = useState([]);

  useEffect(() => {
    fetch('user_data.json')
      .then(response => response.json())
      .then(userData => setContacts(userData.contacts))
      .catch(err => console.log(err));
  }, []);

  useEffect(() => {
    getFetch('get_all_chat_names')
      .then(chatNames => setAllChatNames(JSON.parse(chatNames)))
      .catch(err => console.log(err));

    getFetch('get_all_phone_numbers')
      .then(phoneNumbers => setAllPhoneNumbers(formatNumbers(JSON.parse(phoneNumbers))))
      .catch(err => console.log(err));
  }, []);

  if (allChatNames.length === 0 || allPhoneNumbers.length === 0) {
    return (
      <div className='loading-gif'>
        <Loader
          type="Oval"
          color="#1982fc"
          height={200}
          width={200}
        />
      </div>
    );
  }

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
          allChatNames={allChatNames}
          allPhoneNumbers={allPhoneNumbers}
        />
      );

    default:
      return (
        <ContactsPage
          contacts={contacts}
          allChatNames={allChatNames}
          allPhoneNumbers={allPhoneNumbers}
        />
      );
  }
}

export default Page;
