const addContact = (name, number) => {
  fetch();
};

const editContact = (name, number) => {
  fetch();
};

const deleteContact = (name, number) => {
  fetch();
};

const Contact = ({ name, number }) => {
  return (
    <li
      className='contact'
      onClick={() => editContact(name, number)}
    >
      <p className='contact-name'>
        {name}
      </p>
      {number ? <p className='contact-number'>{number}</p> : ''}
      <p
        className='x-btn'
        onClick={() => deleteContact(name, number)}
      >
        &#x2715;
      </p>
    </li>
  )
};

const ContactsPage = ({ contacts, refetchContacts, allChatNames, allPhoneNumbers }) => (
  <div className='page'>
    <div>
      <div className='contacts-section-header'>
        <h3>
          Group Chats
        </h3>
        <p>
          &#x2795; Add Group Chat
        </p>
      </div>
      <ul className='contact-list'>
        {
          Object.keys(contacts).filter(name => contacts[name] === 'group')
            .map(name => <Contact key={name} name={name} />)
        }
      </ul>
    </div>
    <div>
      <div className='contacts-section-header'>
        <h3>
          Contacts
        </h3>
        <p>
          &#x2795; Add Contact
        </p>
      </div>
      <ul className='contact-list'>
        {
          Object.keys(contacts).filter(name => contacts[name] !== 'group')
            .map(name => <Contact key={name} name={name} number={contacts[name]} />)
        }
      </ul>
    </div>
  </div >
);

export default ContactsPage;
