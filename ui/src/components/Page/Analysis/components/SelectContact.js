const SelectContact = ({ contacts, setContactName, setGroup }) => {
  const groupOptions = Object.keys(contacts).filter(name => contacts[name] === 'group')
    .map(name => (
      <option key={name} value={name}>
        {name}
      </option>
    ));

  const contactOptions = Object.keys(contacts).filter(name => contacts[name] !== 'group')
    .map(name => (
      <option key={name} value={name}>
        {name}
      </option>
    ));

  return (
    <select className='select' defaultValue='none' onChange={(event) => {
      setContactName(event.target.value);
      if (contacts[event.target.value] === 'group') {
        setGroup(true);
      } else {
        setGroup(false);
      }
    }}>
      <option value='none' disabled={true}>Select a contact</option>

      <optgroup label='Group Chats'>
        {groupOptions}
      </optgroup>

      <optgroup label='Contacts'>
        {contactOptions}
      </optgroup>
    </select>
  );
};

export default SelectContact;
