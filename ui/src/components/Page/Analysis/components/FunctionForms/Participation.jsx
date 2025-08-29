import React from "react";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";
import Tooltip from "components/common/Tooltip";

const ParticipationForm = () => {
  const { minutesThreshold, setMinutesThreshold } = useAnalysisForm(
    useShallow((s) => ({ minutesThreshold: s.minutesThreshold, setMinutesThreshold: s.setMinutesThreshold }))
  );
  return (
    <div className="input-div">
      <p className="m-0 text-sm text-slate-700 flex items-center gap-2">
        New conversation gap (minutes)
        <Tooltip text={"If the time since the previous message exceeds this many minutes, classify the next message as the start of a new conversation."} />
      </p>
      <div className="mt-1">
        <input
          type="number"
          min="1"
          step="1"
          value={minutesThreshold ?? ""}
          onChange={(e) => setMinutesThreshold(e.target.valueAsNumber)}
          className="border border-slate-300 rounded px-3 py-2 text-sm w-28 focus:outline-none focus:ring-2 focus:ring-slate-300"
          placeholder="e.g., 30"
        />
      </div>
    </div>
  );
};

export default ParticipationForm;
