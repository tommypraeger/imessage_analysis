import { addArg, removeArg } from '../../utils';

const handleChange = (event, setFuncArgs) => {
  removeArg(setFuncArgs, 'day');
  removeArg(setFuncArgs, 'week');
  removeArg(setFuncArgs, 'month');
  removeArg(setFuncArgs, 'year');
  addArg(setFuncArgs, event.target.value, '');
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
            addArg(setFuncArgs, 'graph-individual', '')
          } else {
            removeArg(setFuncArgs, 'graph-individual')
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
