import { getCategories } from "../utils";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";

const SelectOutput = () => {
  const { outputType, setOutputType, func, setCategories, setCategory, graphIndividual } = useAnalysisForm(
    useShallow((s) => ({
      outputType: s.outputType,
      setOutputType: s.setOutputType,
      func: s.func,
      setCategories: s.setCategories,
      setCategory: s.setCategory,
      graphIndividual: s.graphIndividual,
    }))
  );

  return (
    <select
      className="select"
      defaultValue="none"
      onChange={(event) => {
        const nextOutput = event.target.value;
        setOutputType(nextOutput);
        if (func !== "") {
          getCategories(func, nextOutput, graphIndividual, setCategories, setCategory);
        }
      }}
    >
    <option value="table">Table</option>

    <option value="graph">Line Graph</option>
    </select>
  );
};

export default SelectOutput;
