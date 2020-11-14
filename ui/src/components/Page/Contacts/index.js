import React, { useState, useEffect } from 'react';
import Loader from 'react-loader-spinner';
import AddContactModal from './components/AddContactModal';
import AddGroupChatModal from './components/AddGroupChatModal';
import Contact from './components/Contact';
import { getFetch, formatNumbers } from '../utils';

const ContactsPage = ({ contacts }) => {
  const [addContactModalOpen, setAddContactModalOpen] = useState(false);
  const [addGroupChatModalOpen, setAddGroupChatModalOpen] = useState(false);
  const [allChatNames, setAllChatNames] = useState([]);
  const [allPhoneNumbers, setAllPhoneNumbers] = useState([]);

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

  return (
    <div className='page'>
      <AddContactModal
        open={addContactModalOpen}
        setOpen={setAddContactModalOpen}
        allPhoneNumbers={allPhoneNumbers}
      />
      <AddGroupChatModal
        open={addGroupChatModalOpen}
        setOpen={setAddGroupChatModalOpen}
        allChatNames={allChatNames}
      />
      <div>
        <div className='contacts-section-header'>
          <h3>
            Group Chats
          </h3>
          <p onClick={() => setAddGroupChatModalOpen(true)}>
            &#x2795; Add Group Chat
          </p>
        </div>
        <ul className='contact-list'>
          {
            Object.keys(contacts).filter(name => contacts[name] === 'group')
              .map(name =>
                <Contact
                  key={name}
                  name={name}
                  allChatNames={allChatNames}
                  allPhoneNumbers={allPhoneNumbers}
                />)
          }
        </ul>
      </div >
      <div>
        <div className='contacts-section-header'>
          <h3>
            Contacts
          </h3>
          <p onClick={() => setAddContactModalOpen(true)} >
            &#x2795; Add Contact
          </p>
        </div>
        <ul className='contact-list'>
          {
            Object.keys(contacts).filter(name => contacts[name] !== 'group')
              .map(name => <Contact
                key={name}
                name={name}
                number={contacts[name]}
                allChatNames={allChatNames}
                allPhoneNumbers={allPhoneNumbers}
              />)
          }
        </ul>
      </div>
    </div >
  );
};

export default ContactsPage;
