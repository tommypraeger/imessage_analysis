import { useMemo } from "react";
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
  const DateField = ({ label, selectedDate, setDate, placeholder }) => {
    const formatDate = (d) => {
      if (!(d instanceof Date)) return "";
      const y = d.getFullYear();
      const m = String(d.getMonth() + 1).padStart(2, "0");
      const day = String(d.getDate()).padStart(2, "0");
      return `${y}-${m}-${day}`;
    };

    const initial = useMemo(() => (selectedDate ? formatDate(selectedDate) : ""), [selectedDate]);

    const tryCommit = (s) => {
      if (!s) {
        setDate("");
        return;
      }
      if (/^\d{4}-\d{2}-\d{2}$/.test(s)) {
        const [y, m, d] = s.split("-").map((n) => parseInt(n, 10));
        const dt = new Date(y, m - 1, d);
        if (dt.getFullYear() === y && dt.getMonth() === m - 1 && dt.getDate() === d) {
          setDate(dt);
        }
      }
    };

    return (
      <div className="flex items-center gap-2">
        <p className="m-0 text-sm text-slate-700">{label}:</p>
        <input
          key={initial}
          type="date"
          defaultValue={initial}
          onBlur={(e) => tryCommit(e.target.value)}
          placeholder={placeholder || "YYYY-MM-DD"}
          className="border border-slate-300 rounded px-3 py-2 text-sm bg-white"
        />
      </div>
    );
  };
  return (
    <div className="input-div mt-2">
      <div className="text-sm font-medium text-slate-700 mb-1">Date Range</div>
      <div className="flex flex-wrap items-center gap-4">
        <DateField label="Start" selectedDate={startDate} setDate={setStartDate} placeholder="YYYY-MM-DD" />
        <DateField label="End" selectedDate={endDate} setDate={setEndDate} placeholder="YYYY-MM-DD" />
      </div>
    </div>
  );
};

export default DateForm;
