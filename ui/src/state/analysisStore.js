import { create } from "zustand";

const initialState = {
  contactName: "",
  group: false,
  csv: false,
  csvFileName: "",
  func: "",
  funcArgs: {},
  outputType: "table",
  categories: [],
  category: "",
  startDate: "",
  endDate: "",
  response: {},
  reactionType: "all",
};

const useAnalysisForm = create((set, get) => ({
  ...initialState,

  // Global setters
  setContactName: (name) => set({ contactName: name }),
  setGroup: (val) => set({ group: !!val }),
  setCsv: (val) => set({ csv: !!val }),
  setCsvFileName: (name) => set({ csvFileName: name || "" }),
  setFunc: (func) => set({ func }),
  setOutputType: (outputType) => set({ outputType }),
  setCategories: (categories) => set({ categories }),
  setCategory: (category) => set({ category }),
  setStartDate: (date) => set({ startDate: date }),
  setEndDate: (date) => set({ endDate: date }),
  setResponse: (resp) => set({ response: resp }),
  setReactionType: (val) => set({ reactionType: val }),

  // funcArgs compatibility during migration
  setFuncArgs: (updater) => {
    const prev = get().funcArgs;
    const next = typeof updater === "function" ? updater(prev) : updater;
    set({ funcArgs: next || {} });
  },

  reset: () => set({ ...initialState }),
}));

export default useAnalysisForm;
