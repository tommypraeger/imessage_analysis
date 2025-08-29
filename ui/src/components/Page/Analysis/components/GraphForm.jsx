import { useEffect } from "react";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";
import useAnalysisRunner from "../useAnalysisRunner";
import Tooltip from "components/common/Tooltip";

const GraphFormSection = () => {
  const { outputType, graphTimeInterval, setGraphTimeInterval } = useAnalysisForm(
    useShallow((s) => ({
      outputType: s.outputType,
      graphTimeInterval: s.graphTimeInterval,
      setGraphTimeInterval: s.setGraphTimeInterval,
    }))
  );
  useEffect(() => {
    if (outputType === "graph" && !graphTimeInterval) {
      setGraphTimeInterval("month");
    }
  }, [setGraphTimeInterval, outputType, graphTimeInterval]);
  if (outputType === "graph") {
    return (
      <div className="input-div">
        <GraphForm />
      </div>
    );
  }
  return <div />;
};

const GraphForm = () => {
  const { func, graphIndividual, setCategory, setGraphIndividual, setGraphTimeInterval, graphTimeInterval } = useAnalysisForm(
    useShallow((s) => ({
      func: s.func,
      graphIndividual: s.graphIndividual,
      setCategory: s.setCategory,
      setGraphIndividual: s.setGraphIndividual,
      setGraphTimeInterval: s.setGraphTimeInterval,
      graphTimeInterval: s.graphTimeInterval,
    }))
  );
  const { fetchCategories } = useAnalysisRunner();

  const TimeIntervalRadioGroup = ({ options }) => (
    <div className="flex items-center gap-4">
      {options.map((opt) => (
        <label key={opt.value} className="inline-flex items-center gap-2 cursor-pointer select-none">
          <input
            className="h-4 w-4 rounded-full accent-slate-900"
            type="radio"
            name="time-interval"
            value={opt.value}
            checked={graphTimeInterval === opt.value}
            onChange={(e) => setGraphTimeInterval(e.target.value)}
          />
          <span className="text-sm text-slate-800">{opt.label}</span>
        </label>
      ))}
    </div>
  );

  return (
  <div>
    <div className="input-div mb-2 flex items-center gap-2">
      <p className="m-0 flex items-center">
        Graph each person individually?
        <Tooltip text={"Shows a separate line for each member instead of only the Total aggregation."} />
      </p>
      <input
        type="checkbox"
        className="h-4 w-4 rounded accent-slate-900"
        checked={!!graphIndividual}
        onChange={(event) => {
          setCategory("");
          fetchCategories(func, "graph", event.target.checked);
          setGraphIndividual(event.target.checked);
        }}
      />
    </div>
    <div className="input-div">
      <p className="inline-block mr-2">Group messages by:</p>
      <TimeIntervalRadioGroup
        options={[
          { value: "day", label: "Day" },
          { value: "week", label: "Week" },
          { value: "month", label: "Month" },
          { value: "year", label: "Year" },
        ]}
      />
    </div>
  </div>
  );
};

export default GraphFormSection;
