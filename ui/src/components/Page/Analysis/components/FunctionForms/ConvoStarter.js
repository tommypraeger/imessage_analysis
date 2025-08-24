import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";

const ConvoStarterForm = () => {
  const { minutesThreshold, setMinutesThreshold } = useAnalysisForm(
    useShallow((s) => ({ minutesThreshold: s.minutesThreshold, setMinutesThreshold: s.setMinutesThreshold }))
  );
  return (
    <div className="input-div">
      <p>
        Time (in minutes) after the previous message for a new message to be classified as a new
        conversation:
      </p>
      <input type="number" min="1" value={minutesThreshold || 60} onChange={(e) => setMinutesThreshold(e.target.valueAsNumber)} />
    </div>
  );
};

export default ConvoStarterForm;
