import React, { useState } from 'react';
import FunctionForm from './components/FunctionForms';
import SelectContact from './components/SelectContact';
import SelectFunction from './components/SelectFunction';

const AnalysisPage = ({ contacts }) => {
  const [contactName, setContactName] = useState('');
  const [group, setGroup] = useState(false);
  const [func, setFunc] = useState('');
  const [funcArgs, setFuncArgs] = useState({});

  // TODO: Add calendars to choose from-date and to-date
  console.log(funcArgs)

  return (
    <div>
      <div className='input-div'>
        <h2>Analysis for</h2>
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
    </div>
  );
};

export default AnalysisPage;
