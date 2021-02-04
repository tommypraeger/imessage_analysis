const SelectContact = ({ contacts, setContactName, setGroup, setCsv }) => {
  const groupOptions = Object.keys(contacts)
    .filter(name => contacts[name] === 'group')
    .sort()
    .map(name => (
      <option key={name} value={name}>
        {name}
      </option>
    ));

  const contactOptions = Object.keys(contacts)
    .filter(name => contacts[name] !== 'group')
    .sort()
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
      if (event.target.value === 'messages.csv') {
        setCsv(true)
      } else {
        setCsv(false);
      }
    }}>
      <option value='none' disabled={true}>Select a contact</option>

      <optgroup label='Messages CSV'>
        <option value='messages.csv'>
          messages.csv
        </option>
      </optgroup>

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
