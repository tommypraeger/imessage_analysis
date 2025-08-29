import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";
import SelectMenu from "components/common/SelectMenu";

const SelectCategory = () => {
  const { outputType, setCategory, categories, category } = useAnalysisForm(
    useShallow((s) => ({
      outputType: s.outputType,
      setCategory: s.setCategory,
      categories: s.categories,
      category: s.category,
    }))
  );

  if (outputType === "graph") {
    return (
      <div className="input-div">
        <h2 className="text-sm font-medium text-slate-700 mb-1">Category</h2>
        <SelectMenu
          value={category || categories[0]}
          onChange={(val) => setCategory(val)}
          options={(categories || []).map((c) => ({ value: c, label: c }))}
          placeholder="Select category"
        />
      </div>
    );
  }
  return <div />;
};

export default SelectCategory;
