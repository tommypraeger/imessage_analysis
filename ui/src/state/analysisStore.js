import { create } from "zustand";

const initialState = {
  contactName: "",
  group: false,
  csv: false,
  csvFileName: "",
  func: "",
  outputType: "table",
  categories: [],
  category: "",
  startDate: "",
  endDate: "",
  response: {},
  reactionType: "all",
  minutesThreshold: 60,
  mimeType: "image/png",
  phrase: "",
  phraseSeparate: false,
  phraseCaseSensitive: false,
  phraseRegex: false,
  graphIndividual: false,
  graphTimeInterval: "",
  // Scatter
  scatterMode: "preset", // 'preset' | 'custom'
  scatterPreset: "lfwt",
  scatterXFunction: "",
  scatterXCategory: "",
  scatterYFunction: "",
  scatterYCategory: "",
  scatterRegression: false,
  scatterResiduals: false,
  scatterAlpha: 1,
  scatterBeta: 1,
};

const useAnalysisForm = create((set, get) => ({
  ...initialState,

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
  setMinutesThreshold: (val) =>
    set({ minutesThreshold: Number.isNaN(val) ? undefined : val }),
  setMimeType: (val) => set({ mimeType: val }),
  setPhrase: (val) => set({ phrase: val }),
  setPhraseSeparate: (val) => set({ phraseSeparate: !!val }),
  setPhraseCaseSensitive: (val) => set({ phraseCaseSensitive: !!val }),
  setPhraseRegex: (val) => set({ phraseRegex: !!val }),
  setGraphIndividual: (val) => set({ graphIndividual: !!val }),
  setGraphTimeInterval: (val) => set({ graphTimeInterval: val }),
  // Scatter setters
  setScatterMode: (val) => set({ scatterMode: val }),
  setScatterPreset: (val) => set({ scatterPreset: val }),
  setScatterXFunction: (val) => set({ scatterXFunction: val }),
  setScatterXCategory: (val) => set({ scatterXCategory: val }),
  setScatterYFunction: (val) => set({ scatterYFunction: val }),
  setScatterYCategory: (val) => set({ scatterYCategory: val }),
  setScatterRegression: (val) => set({ scatterRegression: !!val }),
  setScatterResiduals: (val) => set({ scatterResiduals: !!val }),
  setScatterAlpha: (val) => set({ scatterAlpha: val }),
  setScatterBeta: (val) => set({ scatterBeta: val }),

  getAnalyzeDisabled: () => {
    const s = get();
    const { contactName, func, outputType, category, csv, csvFileName } = s;
    if (!contactName) return true;
    // For scatter we don't require primary func selection
    if (outputType !== "scatter" && !func) return true;
    if (func === "phrase" && !s.phrase) return true;
    if (func === "mime_type" && !s.mimeType) return true;
    if ((func === "message_series" || func === "conversation_starter" || func === "participation") && !s.minutesThreshold)
      return true;
    if (outputType === "graph" && (!category || !s.graphTimeInterval)) return true;
    if (outputType === "scatter") {
      if (s.scatterMode === "preset") {
        if (!s.scatterPreset) return true;
      } else {
        if (!s.scatterXFunction || !s.scatterXCategory || !s.scatterYFunction || !s.scatterYCategory) return true;
      }
    }
    if (csv && csvFileName === "") return true;
    return false;
  },

  reset: () => set({ ...initialState }),
}));

export default useAnalysisForm;
