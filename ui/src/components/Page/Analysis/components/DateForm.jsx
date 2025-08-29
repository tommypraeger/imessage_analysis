import DatePicker from "react-datepicker";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";

const DateForm = () => {
  const { startDate, endDate, setStartDate, setEndDate } = useAnalysisForm(
    useShallow((s) => ({
      startDate: s.startDate,
      endDate: s.endDate,
      setStartDate: s.setStartDate,
      setEndDate: s.setEndDate,
    }))
  );
  const DateField = ({ label, selected, onChange, placeholder }) => (
    <div className="date-input">
      <p>{label}:</p>
      <DatePicker
        dateFormat="yyyy-MM-dd"
        selected={selected}
        onChange={onChange}
        placeholderText={placeholder}
        isClearable={true}
      />
    </div>
  );
  return (
    <div className="input-div">
      <p>Limit dates to...</p>
      <DateField label="Start" selected={startDate} onChange={setStartDate} placeholder="No start limit" />
      <DateField label="End" selected={endDate} onChange={setEndDate} placeholder="No end limit" />
    </div>
  );
};

export default DateForm;
