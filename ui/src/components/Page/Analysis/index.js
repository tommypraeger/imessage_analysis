import React, { useState, useEffect } from "react";
import DateForm from "./components/DateForm";
import FunctionForm from "./components/FunctionForms";
import GraphFormSection from "./components/GraphForm";
import SelectCategory from "./components/SelectCategory";
import SelectContact from "./components/SelectContact";
import SelectFunction from "./components/SelectFunction";
import SelectOutput from "./components/SelectOutput";
import Analysis from "./components/Analysis";
import { getCategories, runAnalysis } from "./utils";

const AnalysisPage = ({ contacts, fetchesInProgress, setFetchesInProgress }) => {
  const [contactName, setContactName] = useState("");
  const [group, setGroup] = useState(false);
  const [csv, setCsv] = useState(false);
  const [csvFileName, setCsvFileName] = useState("");
  const [func, setFunc] = useState("");
  const [funcArgs, setFuncArgs] = useState({});
  const [outputType, setOutputType] = useState("table");
  const [categories, setCategories] = useState([]);
  const [category, setCategory] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [response, setResponse] = useState({});
  const [fetchSeconds, setFetchSeconds] = useState(0);
  const [counterId, setCounterId] = useState(0);
  const [isCounterSet, setIsCounterSet] = useState(false);

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
          <SelectContact
            contacts={contacts}
            setContactName={setContactName}
            setGroup={setGroup}
            setCsv={setCsv}
          />
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
          <SelectFunction
            outputType={outputType}
            funcArgs={funcArgs}
            setFunc={setFunc}
            setFuncArgs={setFuncArgs}
            setCategory={setCategory}
            setCategories={setCategories}
          />
        </div>
        {func === "" ? (
          ""
        ) : (
          <div className="select-div">
            <FunctionForm func={func} setFuncArgs={setFuncArgs} />
          </div>
        )}
        <div className="input-div">
          <h2>Output:</h2>
          <SelectOutput
            outputType={outputType}
            setOutputType={setOutputType}
            setCategory={setCategory}
            categories={categories}
            funcArgs={funcArgs}
            func={func}
            getCategories={getCategories}
            setCategories={setCategories}
          />
        </div>
        <SelectCategory outputType={outputType} setCategory={setCategory} categories={categories} />
        <GraphFormSection
          func={func}
          outputType={outputType}
          setFuncArgs={setFuncArgs}
          setCategory={setCategory}
          setCategories={setCategories}
        />
        <DateForm
          startDate={startDate}
          endDate={endDate}
          setStartDate={setStartDate}
          setEndDate={setEndDate}
        />
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
              startDate,
              endDate,
              setFetchesInProgress,
              setResponse
            );
          }}
          disabled={
            !contactName ||
            !func ||
            (func === "phrase" && !funcArgs.phrase) ||
            (func === "mime_type" && !funcArgs["mime-type"]) ||
            ((func === "message_series" ||
              func === "conversation_starter" ||
              func === "participation") &&
              !funcArgs["minutes-threshold"]) ||
            (outputType === "graph" && (!category || !("graph-time-interval" in funcArgs))) ||
            (csv && csvFileName === "")
          }
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
          fetchesInProgress={fetchesInProgress}
          fetchSeconds={fetchSeconds}
        />
      </div>
    </div>
  );
};

export default AnalysisPage;
