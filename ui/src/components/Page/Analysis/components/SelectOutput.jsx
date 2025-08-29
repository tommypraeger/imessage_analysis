import { useEffect } from "react";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";
import useAnalysisRunner from "../useAnalysisRunner";
import SelectMenu from "components/common/SelectMenu";

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

  const graphDisabled = func === "reaction_matrix";

  // If reaction_matrix is selected while on graph, switch back to table
  useEffect(() => {
    if (graphDisabled && outputType === "graph") {
      setOutputType("table");
    }
  }, [graphDisabled]);

  return (
    <>
    <h2 className="text-sm font-medium text-slate-700 mb-1">Output Type</h2>
    <SelectMenu
      value={outputType}
      onChange={(val) => {
        if (val === "graph" && graphDisabled) return;
        setOutputType(val);
        if (func !== "") {
          fetchCategories(func, val, graphIndividual);
        }
      }}
      options={[
        { value: "table", label: "Table" },
        { value: "graph", label: "Line Graph", disabled: graphDisabled },
      ]}
      placeholder="Select output"
    />
    </>
  );
};

export default SelectOutput;
