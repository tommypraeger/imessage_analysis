import { Line } from "react-chartjs-2";
import { useEffect, useMemo, useState } from "react";
import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";

// https://stackoverflow.com/a/67143648
// eslint-disable-next-line no-unused-vars
import Chart from "chart.js/auto";

const LineGraph = ({ data, category, func }) => {
  const { phrase, mimeType } = useAnalysisForm(
    useShallow((s) => ({ phrase: s.phrase, mimeType: s.mimeType }))
  );

  const computeTitle = (cat, f, phr, mime) => {
    if (f === "phrase") return cat.replace("the entered phrase", `"${phr || ""}"`);
    if (f === "mime_type") return cat.replace("the selected file type", `"${mime || ""}"`);
    return cat;
  };

  // Freeze the title for the current analysis result; update only when new data arrives
  const initialTitle = useMemo(() => computeTitle(category, func, phrase, mimeType), [data]);
  const [title, setTitle] = useState(initialTitle);
  useEffect(() => {
    setTitle(computeTitle(category, func, phrase, mimeType));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data]);
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
