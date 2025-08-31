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
  const DateField = ({ label, selected, onChange, placeholder }) => {
    const value = selected ? new Date(selected).toISOString().slice(0, 10) : "";
    return (
      <div className="flex items-center gap-2">
        <p className="m-0 text-sm text-slate-700">{label}:</p>
        <input
          type="date"
          value={value}
          onChange={(e) => onChange(e.target.value ? new Date(e.target.value) : "")}
          placeholder={placeholder}
          className="border border-slate-300 rounded px-3 py-2 text-sm bg-white"
        />
      </div>
    );
  };
  return (
    <div className="input-div mt-2">
      <div className="text-sm font-medium text-slate-700 mb-1">Date Range</div>
      <div className="flex flex-wrap items-center gap-4">
        <DateField label="Start" selected={startDate} onChange={setStartDate} placeholder="No start limit" />
        <DateField label="End" selected={endDate} onChange={setEndDate} placeholder="No end limit" />
      </div>
    </div>
  );
};

export default DateForm;
