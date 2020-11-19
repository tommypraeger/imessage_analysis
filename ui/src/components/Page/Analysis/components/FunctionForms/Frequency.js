const handleChange = (event, setFuncArgs) => {
  setFuncArgs(args => {
    const newArgs = Object.assign({}, args);
    delete newArgs['day'];
    delete newArgs['week'];
    delete newArgs['month'];
    delete newArgs['year'];
    Object.assign(newArgs, { [event.target.value]: '' })
    return newArgs
  });
};

const FrequencyForm = ({ setFuncArgs }) => (
  <div>
    <div className='input-div'>
      <p>
        Graph each person individually (as opposed to just the total):
        </p>
      <input
        type='checkbox'
        className='checkbox'
        onChange={(event) => {
          if (event.target.checked) {
            setFuncArgs(args => Object.assign(
              {},
              args,
              { 'graph-individual': '' })
            );
          } else {
            setFuncArgs(args => {
              const newArgs = Object.assign({}, args);
              delete newArgs['graph-individual'];
              return newArgs;
            })
          }
        }}
      />
    </div>
    <div className='input-div'>
      <p>
        Group messages by:
      </p>
      <input
        className='radio'
        type='radio'
        value='day'
        name='time-period'
        onChange={(event) => handleChange(event, setFuncArgs)}
      />Day
      <input
        className='radio'
        type='radio'
        value='week'
        name='time-period'
        onChange={(event) => handleChange(event, setFuncArgs)}
      />Week
      <input
        className='radio'
        type='radio'
        value='month'
        name='time-period'
        onChange={(event) => handleChange(event, setFuncArgs)}
      />Month
      <input
        className='radio'
        type='radio'
        value='year'
        name='time-period'
        onChange={(event) => handleChange(event, setFuncArgs)}
      />Year
    </div>
  </div>
);

export default FrequencyForm;
