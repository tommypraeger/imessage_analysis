import React, { useEffect } from 'react';

const PhraseForm = ({ setFuncArgs }) => {
  useEffect(() => {
    setFuncArgs({ 'phrase': '' })
  }, [setFuncArgs]);

  return (
    <div>
      <div className='input-div'>
        <p>
          Phrase to search for:
        </p>
        <input
          type='text'
          onChange={(event) =>
            setFuncArgs(args => Object.assign(
              {},
              args,
              { 'phrase': event.target.value })
            )
          }
        />
      </div>
      <div className='input-div'>
        <p>
          Search whole words (do not include results if phrase is within a larger word):
        </p>
        <input
          type='checkbox'
          className='checkbox'
          onChange={(event) => {
            if (event.target.checked) {
              setFuncArgs(args => Object.assign(
                {},
                args,
                { 'separate': '' })
              );
            } else {
              setFuncArgs(args => {
                const newArgs = Object.assign({}, args);
                delete newArgs.separate;
                return newArgs;
              })
            }
          }}
        />
      </div>
      <div className='input-div'>
        <p>
          Case-sensitive search:
        </p>
        <input
          type='checkbox'
          className='checkbox'
          onChange={(event) => {
            if (event.target.checked) {
              setFuncArgs(args => Object.assign(
                {},
                args,
                { 'case-sensitive': '' })
              );
            } else {
              setFuncArgs(args => {
                const newArgs = Object.assign({}, args);
                delete newArgs['case-sensitive'];
                return newArgs;
              })
            }
          }}
        />
      </div>
    </div>
  );
};

export default PhraseForm;
