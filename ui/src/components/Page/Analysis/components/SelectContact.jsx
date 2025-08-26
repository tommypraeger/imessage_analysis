import { useShallow } from "zustand/react/shallow";
import useAnalysisForm from "state/analysisStore";

const SelectContact = ({ contacts }) => {
  const { contactName, setContactName, setGroup, setCsv } = useAnalysisForm(
    useShallow((s) => ({
      contactName: s.contactName,
      setContactName: s.setContactName,
      setGroup: s.setGroup,
      setCsv: s.setCsv,
    }))
  );
  const renderOptions = (names) =>
    names
      .sort()
      .map((name) => (
        <option key={name} value={name}>
          {name}
        </option>
      ));

  const groupOptions = renderOptions(
    Object.keys(contacts).filter((name) => contacts[name] === "group")
  );
  const contactOptions = renderOptions(
    Object.keys(contacts).filter((name) => contacts[name] !== "group")
  );

  return (
    <>
      <h2>Analysis for:</h2>
      <select
        className="select"
        value={contactName || "none"}
        onChange={(event) => {
          const val = event.target.value;
          setContactName(val);
          setGroup(contacts[val] === "group");
          setCsv(val === "messages_csv");
        }}
      >
        <option value="none" disabled={true}>
          Select a contact
        </option>

        <optgroup label="Messages CSV">
          <option value="messages_csv">Choose a message CSV file</option>
        </optgroup>

        <optgroup label="Group Chats">{groupOptions}</optgroup>

        <optgroup label="Contacts">{contactOptions}</optgroup>
      </select>
    </>
  );
};

export default SelectContact;
