import { useEffect } from "react";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";
import useAnalysisRunner from "../useAnalysisRunner";
import SelectMenu from "components/common/SelectMenu";
import { getFunctionOptions } from "../functionOptions";

const SelectFunction = () => {
  const { outputType, func, setFunc, setCategory, graphIndividual } = useAnalysisForm(
    useShallow((s) => ({
      outputType: s.outputType,
      func: s.func,
      setFunc: s.setFunc,
      setCategory: s.setCategory,
      graphIndividual: s.graphIndividual,
    }))
  );
  const { fetchCategories } = useAnalysisRunner();

  // Default to 'total' if no function selected yet
  useEffect(() => {
    if (!func) {
      setFunc("total");
      setCategory("");
      fetchCategories("total", outputType, graphIndividual);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const options = getFunctionOptions();

  return (
    <div>
      <h2 className="text-sm font-medium text-slate-700 mb-1">Analysis Type</h2>
      <SelectMenu
        value={func || "total"}
        onChange={(val) => {
          setFunc(val);
          setCategory("");
          fetchCategories(val, outputType, graphIndividual);
        }}
        options={options}
        placeholder="Select function"
      />
    </div>
  );
};

export default SelectFunction;
