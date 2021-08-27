const SelectOutput = ({ outputType, setOutputType, setCategory, categories }) => (
  <select
    className='select'
    defaultValue='none'
    onChange={(event) => {
      setOutputType(event.target.value);
    }}
  >
    <option value='table'>
      Table
    </option>

    <option value='graph'>
      Line Graph
    </option>
  </select>
);

export default SelectOutput;
