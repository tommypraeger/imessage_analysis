import LineGraph from "./LineGraph";
import NativeTable from "./NativeTable";
import { parsePandasHtmlTable, extractNestedTables } from "../utils";
import LoadingSpinner from "components/common/LoadingSpinner";

const Analysis = ({ response, category, func, fetchesInProgress, fetchSeconds }) => {
  if (fetchesInProgress > 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[200px] text-center">
        <LoadingSpinner />
        {fetchSeconds > 1 && (
          <p className="mt-4 text-slate-600">Request has been loading for {fetchSeconds} seconds</p>
        )}
      </div>
    );
  } else if (Object.keys(response).length === 0) {
    return (
      <div className="flex items-center justify-center min-h-[200px] text-slate-500 text-sm">
        Run an analysis to see results here.
      </div>
    );
  } else {
    if ("imagePath" in response) {
      return (
        <div className="space-y-2">
          <img src={response.imagePath} alt={response.title || "Scatter plot"} />
        </div>
      );
    } else if ("htmlTable" in response) {
      const nested = extractNestedTables(response.htmlTable);
      if (nested && nested.length > 0) {
        return (
          <div className="analysis-output space-y-6">
            {nested.map((sec, i) => (
              <div key={i} className="border border-slate-200 rounded">
                <div className="px-3 py-2 text-sm font-medium bg-slate-50 border-b border-slate-200">{sec.name}</div>
                <div className="overflow-x-auto p-3" dangerouslySetInnerHTML={{ __html: sec.html }} />
              </div>
            ))}
          </div>
        );
      }
      const { headers, rows } = parsePandasHtmlTable(response.htmlTable);
      return <NativeTable headers={headers} rows={rows} defaultSortCol={1} />;
    } else if ("graphData" in response) {
      return <LineGraph data={response.graphData} category={category} func={func} />;
    } else if ("errorMessage" in response) {
      return <p className="text-center">{response.errorMessage}</p>;
    } else {
      return <div />;
    }
  }
};

export default Analysis;
