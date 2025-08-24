import { getCategories } from "../utils";
import useAnalysisForm from "../../../../state/analysisStore";
import { useShallow } from "zustand/react/shallow";

const SelectOutput = () => {
  const { outputType, setOutputType, func, funcArgs, setCategories, setCategory } = useAnalysisForm(
    useShallow((s) => ({
      outputType: s.outputType,
      setOutputType: s.setOutputType,
      func: s.func,
      funcArgs: s.funcArgs,
      setCategories: s.setCategories,
      setCategory: s.setCategory,
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
          getCategories(func, nextOutput, funcArgs["graph-individual"], setCategories, setCategory);
        }
      }}
    >
    <option value="table">Table</option>

    <option value="graph">Line Graph</option>
    </select>
  );
};

export default SelectOutput;
