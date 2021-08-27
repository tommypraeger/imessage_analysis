const SelectCategory = ({ outputType, setCategory, categories }) => {
  if (outputType === 'graph') {
    return (
      <div className='input-div'>
        <h2>Category:</h2>
        <SelectCategoryForm
          outputType={outputType}
          setCategory={setCategory}
          categories={categories}
        />
      </div>
    );
  }
  return <div />;
};

const SelectCategoryForm = ({ outputType, setCategory, categories }) => (
  <select
    className='select'
    onChange={(event) => setCategory(event.target.value)}
  >
    {
      categories.map(category => (
        <option value={category}>
          {category}
        </option>
      ))
    }
  </select>
);

export default SelectCategory;
