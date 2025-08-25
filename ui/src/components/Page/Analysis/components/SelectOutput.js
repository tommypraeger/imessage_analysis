import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";
import useAnalysisRunner from "../useAnalysisRunner";

const SelectOutput = () => {
  const { outputType, setOutputType, func, graphIndividual } = useAnalysisForm(
    useShallow((s) => ({
      outputType: s.outputType,
      setOutputType: s.setOutputType,
      func: s.func,
      graphIndividual: s.graphIndividual,
    }))
  );
  const { fetchCategories } = useAnalysisRunner();

  return (
    <>
    <h2>Output:</h2>
    <select
      className="select"
      value={outputType}
      onChange={(event) => {
        const nextOutput = event.target.value;
        setOutputType(nextOutput);
        if (func !== "") {
          fetchCategories(func, nextOutput, graphIndividual);
        }
      }}
    >
    <option value="table">Table</option>

    <option value="graph">Line Graph</option>
    </select>
    </>
  );
};

export default SelectOutput;
