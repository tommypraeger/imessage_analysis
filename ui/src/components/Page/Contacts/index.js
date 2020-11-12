import React, { useState } from 'react';
import AddContactModal from './components/AddContactModal';
import AddGroupChatModal from './components/AddGroupChatModal';
import EditContactModal from './components/EditContactModal';
import EditGroupChatModal from './components/EditGroupChatModal';
import { deleteContact, deleteGroup } from './utils';

const Contact = ({ name, number, allPhoneNumbers, allChatNames }) => {
  const [editContactModalOpen, setEditContactModalOpen] = useState(false);
  const [editGroupChatModalOpen, setEditGroupChatModalOpen] = useState(false);

  return (
    <React.Fragment>
      <EditContactModal
        open={editContactModalOpen}
        setOpen={setEditContactModalOpen}
        name={name}
        number={number}
        allPhoneNumbers={allPhoneNumbers}
      />
      <EditGroupChatModal
        open={editGroupChatModalOpen}
        setOpen={setEditGroupChatModalOpen}
        name={name}
        allChatNames={allChatNames}
      />
      <li
        className='contact'
        onClick={() => {
          if (number) {
            setEditContactModalOpen(true);
          } else {
            setEditGroupChatModalOpen(true);
          }
        }}
      >
        <p className='contact-name'>
          {name}
        </p>
        {number ? <p className='contact-number'>{number}</p> : ''}
        <p
          className='x-btn'
          onClick={(e) => {
            e.stopPropagation();
            if (number) {
              deleteContact(name);
            } else {
              deleteGroup(name);
            }
          }}
        >
          &#x2715;
      </p>
      </li>
    </React.Fragment>
  )
};

const ContactsPage = ({
  contacts, refetchContacts, setRefetchContacts, allChatNames, allPhoneNumbers
}) => {
  const [addContactModalOpen, setAddContactModalOpen] = useState(false);
  const [addGroupChatModalOpen, setAddGroupChatModalOpen] = useState(false);

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
