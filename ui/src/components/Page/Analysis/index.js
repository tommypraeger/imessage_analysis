import { useState, useEffect } from "react";
import DateForm from "./components/DateForm";
import FunctionForm from "./components/FunctionForms";
import GraphFormSection from "./components/GraphForm";
import CsvFilePicker from "./components/CsvFilePicker";
import SelectCategory from "./components/SelectCategory";
import SelectContact from "./components/SelectContact";
import SelectFunction from "./components/SelectFunction";
import SelectOutput from "./components/SelectOutput";
import Analysis from "./components/Analysis";
import useAnalysisRunner from "./useAnalysisRunner";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";

const AnalysisPage = ({ contacts, fetchesInProgress, setFetchesInProgress }) => {
  const { contactName, func, category, analyzeDisabled } = useAnalysisForm(
    useShallow((s) => ({
      contactName: s.contactName,
      func: s.func,
      category: s.category,
      analyzeDisabled: s.getAnalyzeDisabled(),
    }))
  );
  const { run } = useAnalysisRunner();
  const [response, setResponse] = useState({});
  const [fetchSeconds, setFetchSeconds] = useState(0);

  useEffect(() => {
    setResponse({});
  }, [contactName, func, category]);

  // Track fetch duration without extra state flags
  useEffect(() => {
    if (fetchesInProgress > 0) {
      const id = setInterval(() => setFetchSeconds((seconds) => seconds + 1), 1000);
      return () => clearInterval(id);
    }
    setFetchSeconds(0);
  }, [fetchesInProgress]);

  const handleAnalyzeClick = () => {
    setResponse({});
    run(setFetchesInProgress, setResponse);
  };

  return (
    <div>
      <div className="center-content">
        <div className="input-div">
          <SelectContact contacts={contacts} />
        </div>
        <CsvFilePicker />
        <div className="input-div">
          <SelectFunction />
        </div>
        {func && (
          <div className="select-div">
            <FunctionForm />
          </div>
        )}
        <div className="input-div">
          <SelectOutput />
        </div>
        <SelectCategory />
        <GraphFormSection />
        <DateForm />
        <button className="center-btn" onClick={handleAnalyzeClick} disabled={analyzeDisabled}>
          Analyze
        </button>
      </div>
      <Analysis
        response={response}
        category={category}
        func={func}
        fetchesInProgress={fetchesInProgress}
        fetchSeconds={fetchSeconds}
      />
    </div>
  );
};

export default AnalysisPage;
