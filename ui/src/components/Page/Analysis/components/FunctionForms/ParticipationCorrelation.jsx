import React from "react";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";
import Tooltip from "components/common/Tooltip";

const ParticipationCorrelationForm = ({ scope = "primary" }) => {
  const selectors = (s) => {
    if (scope === "scatter-x") {
      return { minutesThreshold: s.scatterXMinutesThreshold, setMinutesThreshold: s.setScatterXMinutesThreshold, excludeReactions: s.scatterExcludeReactions, setExcludeReactions: s.setScatterExcludeReactions };
    }
    if (scope === "scatter-y") {
      return { minutesThreshold: s.scatterYMinutesThreshold, setMinutesThreshold: s.setScatterYMinutesThreshold, excludeReactions: s.scatterExcludeReactions, setExcludeReactions: s.setScatterExcludeReactions };
    }
    return { minutesThreshold: s.minutesThreshold, setMinutesThreshold: s.setMinutesThreshold, excludeReactions: s.excludeReactions, setExcludeReactions: s.setExcludeReactions };
  };

  const { minutesThreshold, setMinutesThreshold, excludeReactions, setExcludeReactions } = useAnalysisForm(
    useShallow(selectors)
  );

  return (
    <div className="input-div space-y-2">
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
      <label className="flex items-center gap-2 text-sm text-slate-700">
        <input
          type="checkbox"
          checked={excludeReactions}
          onChange={(e) => setExcludeReactions(e.target.checked)}
          className="h-4 w-4"
        />
        <span>Exclude reactions</span>
      </label>
    </div>
  );
};

export default ParticipationCorrelationForm;
