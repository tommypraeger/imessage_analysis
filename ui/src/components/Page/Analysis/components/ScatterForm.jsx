import { useEffect, useMemo, useState } from "react";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";
import SelectMenu from "components/common/SelectMenu";
import { getFunctionOptions } from "../functionOptions";
import { postFetch } from "../../utils";

const ScatterFormSection = () => {
  const { outputType } = useAnalysisForm(useShallow((s) => ({ outputType: s.outputType })));
  if (outputType !== "scatter") return <div />;
  return (
    <div className="input-div">
      <ScatterForm />
    </div>
  );
};

const ScatterForm = () => {
  const store = useAnalysisForm(
    useShallow((s) => ({
      scatterMode: s.scatterMode,
      setScatterMode: s.setScatterMode,
      scatterPreset: s.scatterPreset,
      setScatterPreset: s.setScatterPreset,
      scatterRegression: s.scatterRegression,
      setScatterRegression: s.setScatterRegression,
      scatterResiduals: s.scatterResiduals,
      setScatterResiduals: s.setScatterResiduals,
      scatterXFunction: s.scatterXFunction,
      setScatterXFunction: s.setScatterXFunction,
      scatterXCategory: s.scatterXCategory,
      setScatterXCategory: s.setScatterXCategory,
      scatterYFunction: s.scatterYFunction,
      setScatterYFunction: s.setScatterYFunction,
      scatterYCategory: s.scatterYCategory,
      setScatterYCategory: s.setScatterYCategory,
    }))
  );

  const functionOptions = useMemo(() => getFunctionOptions({ forScatter: true }), []);

  const [xCategories, setXCategories] = useState([]);
  const [yCategories, setYCategories] = useState([]);

  // Fetch categories for a function in table mode
  const fetchCategories = (fnName, setCategories) => {
    if (!fnName) return setCategories([]);
    const args = { function: fnName, table: "" };
    postFetch("get_categories", args)
      .then((res) => {
        try {
          const cats = JSON.parse(res);
          setCategories(cats || []);
        } catch (e) {
          setCategories([]);
        }
      })
      .catch(() => setCategories([]));
  };

  useEffect(() => {
    if (store.scatterMode === "custom") fetchCategories(store.scatterXFunction, setXCategories);
  }, [store.scatterMode, store.scatterXFunction]);
  useEffect(() => {
    if (store.scatterMode === "custom") fetchCategories(store.scatterYFunction, setYCategories);
  }, [store.scatterMode, store.scatterYFunction]);

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-4">
        <label className="inline-flex items-center gap-2 cursor-pointer select-none">
          <input
            className="h-4 w-4 rounded-full accent-slate-900"
            type="radio"
            name="scatter-mode"
            value="preset"
            checked={store.scatterMode === "preset"}
            onChange={() => {
              store.setScatterMode("preset");
              // Clear regression/residuals when switching to preset (presets are opinionated)
              store.setScatterRegression(false);
              store.setScatterResiduals(false);
            }}
          />
          <span className="text-sm text-slate-800">Preset</span>
        </label>
        <label className="inline-flex items-center gap-2 cursor-pointer select-none">
          <input
            className="h-4 w-4 rounded-full accent-slate-900"
            type="radio"
            name="scatter-mode"
            value="custom"
            checked={store.scatterMode === "custom"}
            onChange={() => store.setScatterMode("custom")}
          />
          <span className="text-sm text-slate-800">Custom</span>
        </label>
      </div>

      {store.scatterMode === "preset" ? (
        <div className="space-y-2">
          <h3 className="text-sm font-medium text-slate-700">Preset</h3>
          <SelectMenu
            value={store.scatterPreset}
            onChange={(val) => store.setScatterPreset(val)}
            options={[
              { value: "lfwt", label: "LFWT: Leader/Feeder vs Walker/Talker" },
              { value: "rroe", label: "RROE: Reactions Received Over Expected" },
            ]}
            placeholder="Select preset"
          />
        </div>
      ) : (
        <div className="space-y-4">
          <div>
            <h3 className="text-sm font-medium text-slate-700 mb-1">X Axis</h3>
            <div className="grid grid-cols-2 gap-2">
              <SelectMenu
                value={store.scatterXFunction}
                onChange={(val) => {
                  store.setScatterXFunction(val);
                  store.setScatterXCategory("");
                }}
                options={functionOptions.map(({ value, label, desc }) => ({ value, label, desc }))}
                placeholder="Select function"
              />
              <SelectMenu
                value={store.scatterXCategory}
                onChange={(val) => store.setScatterXCategory(val)}
                options={(xCategories || []).map((c) => ({ value: c, label: c }))}
                placeholder="Select category"
              />
            </div>
          </div>
          <div>
            <h3 className="text-sm font-medium text-slate-700 mb-1">Y Axis</h3>
            <div className="grid grid-cols-2 gap-2">
              <SelectMenu
                value={store.scatterYFunction}
                onChange={(val) => {
                  store.setScatterYFunction(val);
                  store.setScatterYCategory("");
                }}
                options={functionOptions.map(({ value, label, desc }) => ({ value, label, desc }))}
                placeholder="Select function"
              />
              <SelectMenu
                value={store.scatterYCategory}
                onChange={(val) => store.setScatterYCategory(val)}
                options={(yCategories || []).map((c) => ({ value: c, label: c }))}
                placeholder="Select category"
              />
            </div>
          </div>
        </div>
      )}

      {store.scatterMode === "custom" && (
        <div className="flex items-center gap-6">
          <label className="inline-flex items-center gap-2 cursor-pointer select-none">
            <input
              type="checkbox"
              className="h-4 w-4 rounded accent-slate-900"
              checked={!!store.scatterRegression}
              onChange={(e) => store.setScatterRegression(!!e.target.checked)}
            />
            <span className="text-sm text-slate-800">Add regression line</span>
          </label>
          <label className="inline-flex items-center gap-2 cursor-pointer select-none">
            <input
              type="checkbox"
              className="h-4 w-4 rounded accent-slate-900"
              checked={!!store.scatterResiduals}
              onChange={(e) => store.setScatterResiduals(!!e.target.checked)}
              disabled={!store.scatterRegression}
            />
            <span className="text-sm text-slate-800">Show residuals</span>
          </label>
        </div>
      )}
    </div>
  );
};

export default ScatterFormSection;
