import { useState, useEffect } from "react";
import DateForm from "./components/DateForm";
import FunctionForm from "./components/FunctionForms";
import GraphFormSection from "./components/GraphForm";
import ScatterFormSection from "./components/ScatterForm";
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
  const { contactName, func, category, analyzeDisabled, outputType } = useAnalysisForm(
    useShallow((s) => ({
      contactName: s.contactName,
      func: s.func,
      category: s.category,
      outputType: s.outputType,
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
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-0">
      <aside className="lg:col-span-4 pr-6">
        <div className="sticky top-4">
          <div className="space-y-4">
            <div className="input-div">
              <SelectContact contacts={contacts} />
            </div>
            <CsvFilePicker />
            <div className="input-div">
              <SelectOutput />
            </div>
            {outputType !== "scatter" && (
              <>
                <div className="input-div">
                  <SelectFunction />
                </div>
                {func && (
                  <div className="select-div">
                    <FunctionForm />
                  </div>
                )}
              </>
            )}
            <SelectCategory />
            <GraphFormSection />
            <ScatterFormSection />
            <DateForm />
            <button
              className="inline-flex items-center px-4 py-2 rounded bg-slate-900 text-white disabled:bg-slate-300"
              onClick={handleAnalyzeClick}
              disabled={analyzeDisabled}
            >
              Analyze
            </button>
          </div>
        </div>
      </aside>
      <main className="lg:col-span-8 lg:border-l border-slate-200 lg:pl-6 min-h-[320px]">
        <Analysis
          response={response}
          category={category}
          func={func}
          fetchesInProgress={fetchesInProgress}
          fetchSeconds={fetchSeconds}
        />
      </main>
    </div>
  );
};

export default AnalysisPage;
