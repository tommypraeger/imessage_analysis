import { useState, useEffect } from "react";
import DateForm from "./components/DateForm";
import FunctionForm from "./components/FunctionForms";
import GraphFormSection from "./components/GraphForm";
import SelectCategory from "./components/SelectCategory";
import SelectContact from "./components/SelectContact";
import SelectFunction from "./components/SelectFunction";
import SelectOutput from "./components/SelectOutput";
import Analysis from "./components/Analysis";
import { getCategories, runAnalysis } from "./utils";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";

const AnalysisPage = ({ contacts, fetchesInProgress, setFetchesInProgress }) => {
  const { contactName, group, csv, csvFileName, setCsvFileName, reactionType, setReactionType, func, outputType, category, funcArgs, setFuncArgs } =
    useAnalysisForm(
      useShallow((s) => ({
        contactName: s.contactName,
        group: s.group,
        csv: s.csv,
        csvFileName: s.csvFileName,
        setCsvFileName: s.setCsvFileName,
        reactionType: s.reactionType,
        setReactionType: s.setReactionType,
        func: s.func,
        outputType: s.outputType,
        category: s.category,
        funcArgs: s.funcArgs,
        setFuncArgs: s.setFuncArgs,
      }))
    );
  // funcArgs managed via store (temporary during migration)
  // outputType managed via store
  // categories and category managed via store inside subcomponents
  // startDate/endDate managed via store
  const [response, setResponse] = useState({});
  const [fetchSeconds, setFetchSeconds] = useState(0);
  const [counterId, setCounterId] = useState(0);
  const [isCounterSet, setIsCounterSet] = useState(false);
  // reactionType managed via store

  useEffect(() => {
    setResponse({});
  }, [contactName, func, funcArgs, category]);

  useEffect(() => {
    if (fetchesInProgress > 0 && !isCounterSet) {
      setCounterId(setInterval(() => setFetchSeconds((seconds) => seconds + 1), 1000));
      setIsCounterSet(true);
    } else if (fetchesInProgress === 0) {
      clearInterval(counterId);
      setIsCounterSet(false);
      setFetchSeconds(0);
    }
  }, [counterId, isCounterSet, fetchesInProgress]);

  return (
    <div>
      <div className="center-content">
        <div className="input-div">
          <h2>Analysis for:</h2>
          <SelectContact contacts={contacts} />
        </div>
        {csv ? (
          <div className="input-div">
            <h4>Messages CSV: </h4>
            <input
              type="file"
              accept="text/csv"
              onChange={(event) => {
                if (event.target.files.length === 1) {
                  setCsvFileName(event.target.files[0].name);
                } else {
                  setCsvFileName("");
                }
              }}
            />
          </div>
        ) : (
          ""
        )}
        <div className="input-div">
          <h2>Function:</h2>
          <SelectFunction />
        </div>
        {func === "" ? (
          ""
        ) : (
          <div className="select-div">
            <FunctionForm />
          </div>
        )}
        <div className="input-div">
          <h2>Output:</h2>
          <SelectOutput />
        </div>
        <SelectCategory />
        <GraphFormSection />
        <DateForm />
        <button
          className="center-btn"
          onClick={() => {
            setResponse({});
            runAnalysis(
              contactName,
              func,
              funcArgs,
              outputType,
              category,
              group,
              csv,
              csvFileName,
              useAnalysisForm.getState().startDate,
              useAnalysisForm.getState().endDate,
              reactionType,
              setFetchesInProgress,
              setResponse
            );
          }}
          disabled={useAnalysisForm((s) => s.getAnalyzeDisabled())}
        >
          Analyze
        </button>
      </div>
      <div>
        <Analysis
          response={response}
          category={category}
          func={func}
          funcArgs={funcArgs}
          reactionType={reactionType}
          fetchesInProgress={fetchesInProgress}
          fetchSeconds={fetchSeconds}
        />
      </div>
    </div>
  );
};

export default AnalysisPage;
