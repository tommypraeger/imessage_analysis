import { useEffect } from "react";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";
import useAnalysisRunner from "../useAnalysisRunner";

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
    <>
      {options.map((opt) => (
        <label key={opt.value} style={{ marginRight: 8 }}>
          <input
            className="radio"
            type="radio"
            name="time-interval"
            value={opt.value}
            checked={graphTimeInterval === opt.value}
            onChange={(e) => setGraphTimeInterval(e.target.value)}
          />
          {opt.label}
        </label>
      ))}
    </>
  );

  return (
  <div>
    <div className="input-div">
      <p>Graph each person individually (as opposed to just the total)?</p>
      <input
        type="checkbox"
        className="checkbox"
        checked={!!graphIndividual}
        onChange={(event) => {
          setCategory("");
          fetchCategories(func, "graph", event.target.checked);
          setGraphIndividual(event.target.checked);
        }}
      />
    </div>
    <div className="input-div">
      <p>Group messages by:</p>
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
