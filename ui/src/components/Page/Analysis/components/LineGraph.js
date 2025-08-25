import { Line } from "react-chartjs-2";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";

// https://stackoverflow.com/a/67143648
// eslint-disable-next-line no-unused-vars
import Chart from "chart.js/auto";

const LineGraph = ({ data, category, func }) => {
  const { phrase, mimeType } = useAnalysisForm(
    useShallow((s) => ({ phrase: s.phrase, mimeType: s.mimeType }))
  );
  const title = func === "phrase"
    ? category.replace("the entered phrase", `"${phrase || ""}"`)
    : func === "mime_type"
      ? category.replace("the selected file type", `"${mimeType || ""}"`)
      : category;
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
            text: title,
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
