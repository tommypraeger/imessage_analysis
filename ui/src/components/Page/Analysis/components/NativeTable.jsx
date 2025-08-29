import { useMemo, useState, useEffect } from "react";

const cellToNumber = (text) => {
  const n = parseFloat(String(text).replace(/[%,\$,\s,]/g, ""));
  return Number.isNaN(n) ? null : n;
};

const NativeTable = ({ headers, rows, defaultSortCol = 1 }) => {
  const [sortCol, setSortCol] = useState(defaultSortCol);
  const [sortDir, setSortDir] = useState("desc"); // default for numeric

  // Adjust default direction based on detected type of the default column
  useEffect(() => {
    const values = rows.map((r) => r?.[defaultSortCol] ?? "");
    const nums = values.map(cellToNumber);
    const isNumeric = nums.every((v) => v !== null);
    setSortDir(isNumeric ? "desc" : "asc");
    setSortCol(defaultSortCol);
  }, [defaultSortCol, rows]);

  const sortedRows = useMemo(() => {
    const col = sortCol ?? 0;
    const dir = sortDir === "asc" ? 1 : -1;
    const nums = rows.map((r) => cellToNumber(r?.[col] ?? ""));
    const isNumeric = nums.every((v) => v !== null);
    const copy = rows.slice();
    copy.sort((a, b) => {
      const av = a?.[col] ?? "";
      const bv = b?.[col] ?? "";
      if (isNumeric) {
        const an = cellToNumber(av) ?? 0;
        const bn = cellToNumber(bv) ?? 0;
        return (an - bn) * dir;
      }
      const as = String(av).toLowerCase();
      const bs = String(bv).toLowerCase();
      if (as < bs) return -1 * dir;
      if (as > bs) return 1 * dir;
      return 0;
    });
    return copy;
  }, [rows, sortCol, sortDir]);

  const onHeaderClick = (idx) => {
    if (idx === sortCol) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      // choose direction by detected type
      const nums = rows.map((r) => cellToNumber(r?.[idx] ?? ""));
      const isNumeric = nums.every((v) => v !== null);
      setSortCol(idx);
      setSortDir(isNumeric ? "desc" : "asc");
    }
  };

  const arrow = (idx) => {
    if (idx !== sortCol) return null;
    return sortDir === "asc" ? "▲" : "▼";
  };

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse">
        <thead>
          <tr>
            {headers.map((h, i) => (
              <th
                key={i}
                className="text-left text-sm font-semibold bg-slate-50 border-b border-slate-200 px-3 py-2 cursor-pointer select-none"
                onClick={() => onHeaderClick(i)}
                aria-sort={sortCol === i ? (sortDir === "asc" ? "ascending" : "descending") : "none"}
                title="Click to sort"
              >
                <span>{h}</span>
                <span className="inline-block ml-1 text-slate-400">{arrow(i)}</span>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sortedRows.map((r, ri) => (
            <tr key={ri} className="hover:bg-slate-50">
              {r.map((c, ci) => (
                <td key={ci} className="text-sm border-b border-slate-100 px-3 py-2">{c}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default NativeTable;

