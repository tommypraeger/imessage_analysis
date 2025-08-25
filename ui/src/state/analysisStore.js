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

  getAnalyzeDisabled: () => {
    const s = get();
    const { contactName, func, outputType, category, csv, csvFileName } = s;
    if (!contactName || !func) return true;
    if (func === "phrase" && !s.phrase) return true;
    if (func === "mime_type" && !s.mimeType) return true;
    if ((func === "message_series" || func === "conversation_starter" || func === "participation") && !s.minutesThreshold)
      return true;
    if (outputType === "graph" && (!category || !s.graphTimeInterval)) return true;
    if (csv && csvFileName === "") return true;
    return false;
  },

  reset: () => set({ ...initialState }),
}));

export default useAnalysisForm;
