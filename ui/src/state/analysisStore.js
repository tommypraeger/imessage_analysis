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
  scatterIdentity: false,
  scatterXPhrase: "",
  scatterXPhraseSeparate: false,
  scatterXPhraseCaseSensitive: false,
  scatterXPhraseRegex: false,
  scatterXMinutesThreshold: 60,
  scatterXMimeType: "image/png",
  scatterYPhrase: "",
  scatterYPhraseSeparate: false,
  scatterYPhraseCaseSensitive: false,
  scatterYPhraseRegex: false,
  scatterYMinutesThreshold: 60,
  scatterYMimeType: "image/png",
  cvaVolumeWeight: 50,
  cvaEfficiencyWeight: 50,
  scatterXCvaVolumeWeight: 50,
  scatterXCvaEfficiencyWeight: 50,
  scatterYCvaVolumeWeight: 50,
  scatterYCvaEfficiencyWeight: 50,
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
  setScatterIdentity: (val) => set({ scatterIdentity: !!val }),
  setScatterAlpha: (val) => set({ scatterAlpha: val }),
  setScatterBeta: (val) => set({ scatterBeta: val }),
  setScatterXPhrase: (val) => set({ scatterXPhrase: val }),
  setScatterXPhraseSeparate: (val) => set({ scatterXPhraseSeparate: !!val }),
  setScatterXPhraseCaseSensitive: (val) => set({ scatterXPhraseCaseSensitive: !!val }),
  setScatterXPhraseRegex: (val) => set({ scatterXPhraseRegex: !!val }),
  setScatterXMinutesThreshold: (val) => set({ scatterXMinutesThreshold: Number.isNaN(val) ? undefined : val }),
  setScatterXMimeType: (val) => set({ scatterXMimeType: val }),
  setScatterYPhrase: (val) => set({ scatterYPhrase: val }),
  setScatterYPhraseSeparate: (val) => set({ scatterYPhraseSeparate: !!val }),
  setScatterYPhraseCaseSensitive: (val) => set({ scatterYPhraseCaseSensitive: !!val }),
  setScatterYPhraseRegex: (val) => set({ scatterYPhraseRegex: !!val }),
  setScatterYMinutesThreshold: (val) => set({ scatterYMinutesThreshold: Number.isNaN(val) ? undefined : val }),
  setScatterYMimeType: (val) => set({ scatterYMimeType: val }),
  setCvaVolumeWeight: (val) => {
    const vol = Math.min(100, Math.max(0, Number(val) || 0));
    set({ cvaVolumeWeight: vol, cvaEfficiencyWeight: 100 - vol });
  },
  setScatterXCvaVolumeWeight: (val) => {
    const vol = Math.min(100, Math.max(0, Number(val) || 0));
    set({ scatterXCvaVolumeWeight: vol, scatterXCvaEfficiencyWeight: 100 - vol });
  },
  setScatterYCvaVolumeWeight: (val) => {
    const vol = Math.min(100, Math.max(0, Number(val) || 0));
    set({ scatterYCvaVolumeWeight: vol, scatterYCvaEfficiencyWeight: 100 - vol });
  },

  getAnalyzeDisabled: () => {
    const s = get();
    const { contactName, func, outputType, category, csv, csvFileName } = s;
    if (!contactName) return true;
    // For scatter we don't require primary func selection
    if (outputType !== "scatter" && !func) return true;
    if (func === "phrase" && !s.phrase) return true;
    if (func === "mime_type" && !s.mimeType) return true;
    if ((func === "message_series" || func === "conversation_starter" || func === "participation" || func === "solo_conversations" || func === "cva_plus" || func === "participation_correlation") && !s.minutesThreshold)
      return true;
    if (outputType === "graph" && (!category || !s.graphTimeInterval)) return true;
    if (outputType === "scatter") {
      if (s.scatterMode === "preset") {
        if (!s.scatterPreset) return true;
      } else {
        if (!s.scatterXFunction || !s.scatterXCategory || !s.scatterYFunction || !s.scatterYCategory) return true;
        const needsMinutes = (fn) => ["message_series", "conversation_starter", "participation"].includes(fn);
        const needsPhrase = (fn) => fn === "phrase";
        const needsMime = (fn) => fn === "mime_type";
        const needsCva = (fn) => fn === "cva_plus";
        if (needsPhrase(s.scatterXFunction) && !s.scatterXPhrase) return true;
        if (needsPhrase(s.scatterYFunction) && !s.scatterYPhrase) return true;
        if (needsMime(s.scatterXFunction) && !s.scatterXMimeType) return true;
        if (needsMime(s.scatterYFunction) && !s.scatterYMimeType) return true;
        if (needsMinutes(s.scatterXFunction) && !s.scatterXMinutesThreshold) return true;
        if (needsMinutes(s.scatterYFunction) && !s.scatterYMinutesThreshold) return true;
        if (needsCva(s.scatterXFunction) && !Number.isFinite(s.scatterXCvaVolumeWeight)) return true;
        if (needsCva(s.scatterYFunction) && !Number.isFinite(s.scatterYCvaVolumeWeight)) return true;
      }
    }
    if (csv && csvFileName === "") return true;
    return false;
  },

  reset: () => set({ ...initialState }),
}));

export default useAnalysisForm;
