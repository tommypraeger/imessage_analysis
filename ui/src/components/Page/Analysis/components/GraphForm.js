import { useEffect } from "react";
import { addArg, removeArg, getCategories } from "../utils";
import useAnalysisForm from "../../../../state/analysisStore";
import { useShallow } from "zustand/react/shallow";

const GraphFormSection = ({ setFuncArgs }) => {
  const { outputType } = useAnalysisForm(useShallow((s) => ({ outputType: s.outputType })));
  useEffect(() => {
    if (outputType === "graph") {
      addArg(setFuncArgs, "graph-time-interval", "month");
    }
  }, [setFuncArgs, outputType]);
  if (outputType === "graph") {
    return (
      <div className="input-div">
        <GraphForm setFuncArgs={setFuncArgs} />
      </div>
    );
  }
  return <div />;
};

const GraphForm = ({ setFuncArgs }) => {
  const { func, setCategory, setCategories } = useAnalysisForm(
    useShallow((s) => ({ func: s.func, setCategory: s.setCategory, setCategories: s.setCategories }))
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
          if (event.target.checked) {
            addArg(setFuncArgs, "graph-individual", "");
          } else {
            removeArg(setFuncArgs, "graph-individual");
          }
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
        onChange={(event) => addArg(setFuncArgs, "graph-time-interval", event.target.value)}
      />
      Day
      <input
        className="radio"
        type="radio"
        value="week"
        name="time-period"
        onChange={(event) => addArg(setFuncArgs, "graph-time-interval", event.target.value)}
      />
      Week
      <input
        className="radio"
        type="radio"
        value="month"
        name="time-period"
        defaultChecked={true}
        onChange={(event) => addArg(setFuncArgs, "graph-time-interval", event.target.value)}
      />
      Month
      <input
        className="radio"
        type="radio"
        value="year"
        name="time-period"
        onChange={(event) => addArg(setFuncArgs, "graph-time-interval", event.target.value)}
      />
      Year
    </div>
  </div>
  );
};

export default GraphFormSection;
