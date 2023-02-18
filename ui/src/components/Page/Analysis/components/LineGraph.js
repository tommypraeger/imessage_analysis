import { Line } from "react-chartjs-2";
import {
  CategoryScale,
  Chart,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip,
} from "chart.js";
// https://stackoverflow.com/a/67143648
Chart.register(CategoryScale, LinearScale, LineElement, Legend, PointElement, Title, Tooltip);

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
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: category,
            font: {
              size: 24,
            },
          },
        },
      }}
    />
  );
};

export default LineGraph;
