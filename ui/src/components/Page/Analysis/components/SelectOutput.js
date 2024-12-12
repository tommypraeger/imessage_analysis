const SelectOutput = ({ outputType, setOutputType, setCategory, categories, funcArgs, func, getCategories, setCategories }) => (
  <select
    className="select"
    defaultValue="none"
    onChange={(event) => {
      setOutputType(event.target.value);
      if (func !== "") {
        getCategories(func, event.target.value, funcArgs["graph-individual"], setCategories, setCategory);
      }
    }}
  >
    <option value="table">Table</option>

    <option value="graph">Line Graph</option>
  </select>
);

export default SelectOutput;
