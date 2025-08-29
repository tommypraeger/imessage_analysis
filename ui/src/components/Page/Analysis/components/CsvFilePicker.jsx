import useAnalysisForm from "state/analysisStore";
import { useShallow } from "zustand/react/shallow";

const CsvFilePicker = () => {
  const { csv, setCsvFileName } = useAnalysisForm(
    useShallow((s) => ({ csv: s.csv, setCsvFileName: s.setCsvFileName }))
  );

  if (!csv) return <></>;

  return (
    <div className="input-div">
      <h4>Messages CSV: </h4>
      <input
        type="file"
        accept="text/csv"
        className="border border-slate-300 rounded px-3 py-2 text-sm bg-white hover:border-slate-400 cursor-pointer"
        onChange={(event) => {
          if (event.target.files.length === 1) {
            setCsvFileName(event.target.files[0].name);
          } else {
            setCsvFileName("");
          }
        }}
      />
    </div>
  );
};

export default CsvFilePicker;
