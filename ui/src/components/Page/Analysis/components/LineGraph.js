import { Line } from "react-chartjs-2";

const LineGraph = ({ data, category, func, funcArgs }) => {
  if (func === "phrase") {
    category = category.replace("the entered phrase", `"${funcArgs.phrase}"`);
  } else if (func === "mime_type") {
    category = category.replace("the selected file type", `"${funcArgs["mime-type"]}"`);
  }
  return (
    <Line
      data={data}
      options={{
        title: {
          display: true,
          text: category,
          fontSize: 24,
          fontStyle: "normal",
        },
      }}
    />
  );
};

export default LineGraph;
