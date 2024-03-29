const SelectCategory = ({ outputType, setCategory, categories }) => {
  if (outputType === "graph") {
    return (
      <div className="input-div">
        <h2>Category:</h2>
        <SelectCategoryForm setCategory={setCategory} categories={categories} />
      </div>
    );
  }
  return <div />;
};

const SelectCategoryForm = ({ setCategory, categories }) => (
  <select className="select" onChange={(event) => setCategory(event.target.value)}>
    {categories.map((category) => (
      <option key={category} value={category}>
        {category}
      </option>
    ))}
  </select>
);

export default SelectCategory;
