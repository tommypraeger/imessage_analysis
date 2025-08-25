import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";
import { getCategories, runAnalysis } from "./utils";

const useAnalysisRunner = () => {
  const store = useAnalysisForm(
    useShallow((s) => ({
      contactName: s.contactName,
      group: s.group,
      csv: s.csv,
      csvFileName: s.csvFileName,
      reactionType: s.reactionType,
      func: s.func,
      outputType: s.outputType,
      category: s.category,
      startDate: s.startDate,
      endDate: s.endDate,
      graphIndividual: s.graphIndividual,
      setCategories: s.setCategories,
      setCategory: s.setCategory,
    }))
  );

  const run = (setFetchesInProgress, setResponse) => {
    runAnalysis(setFetchesInProgress, setResponse);
  };

  const fetchCategories = (nextFunc, nextOutput, nextGraphIndividual) => {
    const func = nextFunc ?? store.func;
    const output = nextOutput ?? store.outputType;
    const graphInd = nextGraphIndividual ?? store.graphIndividual;
    getCategories(func, output, graphInd, store.setCategories, store.setCategory);
  };

  return { run, fetchCategories };
};

export default useAnalysisRunner;
