import React, { useState } from 'react';
import FunctionForm from './components/FunctionForms';
import SelectContact from './components/SelectContact';
import SelectFunction from './components/SelectFunction';

const AnalysisPage = ({ contacts }) => {
  const [contactName, setContactName] = useState('');
  const [group, setGroup] = useState(false);
  const [func, setFunc] = useState('');
  const [funcArgs, setFuncArgs] = useState({});

  console.log(!('day' in funcArgs)
    && !('week' in funcArgs)
    && !('month' in funcArgs)
    && !('year' in funcArgs))

  // TODO: Add calendars to choose from-date and to-date

  return (
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
      <button
        className='center-btn'
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
  );
};

export default AnalysisPage;
