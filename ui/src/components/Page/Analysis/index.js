import React, { useState, useEffect } from 'react';
import DateForm from './components/DateForm';
import FunctionForm from './components/FunctionForms';
import SelectContact from './components/SelectContact';
import SelectFunction from './components/SelectFunction';
import Analysis from './components/Analysis';
import { runAnalysis } from './utils';

const AnalysisPage = ({ contacts }) => {
  const [contactName, setContactName] = useState('');
  const [group, setGroup] = useState(false);
  const [func, setFunc] = useState('');
  const [funcArgs, setFuncArgs] = useState({});
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [response, setResponse] = useState({});
  const [fetchesInProgress, setFetchesInProgress] = useState(0);
  const [fetchSeconds, setFetchSeconds] = useState(0);
  const [counterId, setCounterId] = useState(0);
  const [isCounterSet, setIsCounterSet] = useState(false);

  useEffect(() => {
    setResponse({});
  }, [contactName, func]);

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
      <div className='center-content'>
        <div className='input-div'>
          <h2>Analysis for:</h2>
          <SelectContact
            contacts={contacts}
            setContactName={setContactName}
            setGroup={setGroup}
          />
        </div>
        <div className='input-div'>
          <h2>Function:</h2>
          <SelectFunction setFunc={setFunc} />
        </div>
        {func === '' ? '' : (
          <div className='select-div'>
            <FunctionForm func={func} setFuncArgs={setFuncArgs} />
          </div>
        )}
        <DateForm
          startDate={startDate}
          endDate={endDate}
          setStartDate={setStartDate}
          setEndDate={setEndDate}
        />
        <button
          className='center-btn'
          onClick={() => {
            setResponse({});
            runAnalysis(
              contactName,
              func,
              funcArgs,
              group,
              startDate,
              endDate,
              setFetchesInProgress,
              setResponse
            );
          }}
          disabled={
            !contactName
            || !func
            || (func === 'phrase' && !funcArgs.phrase)
            || (func === 'mime_type' && !funcArgs['mime-type'])
            || (((func === 'all_functions') || (func === 'message_series') || (func === 'convo_starter'))
              && !funcArgs['minutes-threshold'])
            || (func === 'frequency'
              && (!('day' in funcArgs)
                && !('week' in funcArgs)
                && !('month' in funcArgs)
                && !('year' in funcArgs)))
          }
        >Analyze
        </button>
      </div>
      <div>
        <Analysis
          response={response}
          fetchesInProgress={fetchesInProgress}
          fetchSeconds={fetchSeconds}
        />
      </div>
    </div>
  );
};

export default AnalysisPage;
