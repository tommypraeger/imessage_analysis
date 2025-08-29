import { useShallow } from "zustand/react/shallow";
import useAnalysisForm from "state/analysisStore";
import SelectMenu from "components/common/SelectMenu";

const SelectContact = ({ contacts }) => {
  const { contactName, setContactName, setGroup, setCsv } = useAnalysisForm(
    useShallow((s) => ({
      contactName: s.contactName,
      setContactName: s.setContactName,
      setGroup: s.setGroup,
      setCsv: s.setCsv,
    }))
  );
  const groupNames = Object.keys(contacts).filter((name) => contacts[name] === "group").sort();
  const contactNames = Object.keys(contacts).filter((name) => contacts[name] !== "group").sort();
  const groups = [
    { label: "Messages CSV", options: [{ value: "messages_csv", label: "Choose a message CSV file" }] },
    { label: "Group Chats", options: groupNames.map((n) => ({ value: n, label: n })) },
    { label: "Contacts", options: contactNames.map((n) => ({ value: n, label: n })) },
  ];

  return (
    <>
      <h2 className="text-sm font-medium text-slate-700 mb-1">Analysis for:</h2>
      <SelectMenu
        value={contactName || ""}
        onChange={(val) => {
          setContactName(val);
          setGroup(contacts[val] === "group");
          setCsv(val === "messages_csv");
        }}
        groups={groups}
        placeholder="Select a contact"
      />
    </>
  );
};

export default SelectContact;
