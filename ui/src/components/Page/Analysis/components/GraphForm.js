import { useEffect } from "react";
import { getCategories } from "../utils";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";

const GraphFormSection = () => {
  const { outputType, setGraphTimeInterval } = useAnalysisForm(
    useShallow((s) => ({ outputType: s.outputType, setGraphTimeInterval: s.setGraphTimeInterval }))
  );
  useEffect(() => {
    if (outputType === "graph") {
      setGraphTimeInterval("month");
    }
  }, [setGraphTimeInterval, outputType]);
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
  const { func, setCategory, setCategories, setGraphIndividual, setGraphTimeInterval, graphIndividual } = useAnalysisForm(
    useShallow((s) => ({
      func: s.func,
      setCategory: s.setCategory,
      setCategories: s.setCategories,
      setGraphIndividual: s.setGraphIndividual,
      setGraphTimeInterval: s.setGraphTimeInterval,
      graphIndividual: s.graphIndividual,
    }))
  );
  return (
  <div>
    <div className="input-div">
      <p>Graph each person individually (as opposed to just the total)?</p>
      <input
        type="checkbox"
        className="checkbox"
        onChange={(event) => {
          setCategory("");
          getCategories(func, "graph", event.target.checked, setCategories, setCategory);
          setGraphIndividual(event.target.checked);
        }}
      />
    </div>
    <div className="input-div">
      <p>Group messages by:</p>
      <input
        className="radio"
        type="radio"
        value="day"
        name="time-period"
        onChange={(event) => setGraphTimeInterval(event.target.value)}
      />
      Day
      <input
        className="radio"
        type="radio"
        value="week"
        name="time-period"
        onChange={(event) => setGraphTimeInterval(event.target.value)}
      />
      Week
      <input
        className="radio"
        type="radio"
        value="month"
        name="time-period"
        defaultChecked={true}
        onChange={(event) => setGraphTimeInterval(event.target.value)}
      />
      Month
      <input
        className="radio"
        type="radio"
        value="year"
        name="time-period"
        onChange={(event) => setGraphTimeInterval(event.target.value)}
      />
      Year
    </div>
  </div>
  );
};

export default GraphFormSection;
