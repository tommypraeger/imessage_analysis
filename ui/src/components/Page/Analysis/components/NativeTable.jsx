import { useMemo, useState, useEffect } from "react";

const cellToNumber = (text) => {
  const n = parseFloat(String(text).replace(/[%,\$,\s,]/g, ""));
  return Number.isNaN(n) ? null : n;
};

const NativeTable = ({ headers, rows, defaultSortCol = 1, columnWidth = 160 }) => {
  const [sortCol, setSortCol] = useState(defaultSortCol);
  const [sortDir, setSortDir] = useState("desc"); // default for numeric
  const [colWidths, setColWidths] = useState([]);

  // Adjust default direction based on detected type of the default column
  useEffect(() => {
    const values = rows.map((r) => r?.[defaultSortCol] ?? "");
    const nums = values.map(cellToNumber);
    const isNumeric = nums.every((v) => v !== null);
    setSortDir(isNumeric ? "desc" : "asc");
    setSortCol(defaultSortCol);
  }, [defaultSortCol, rows]);

  useEffect(() => {
    setColWidths((prev) => {
      if (prev.length === headers.length && prev.length > 0) return prev;
      return new Array(headers.length).fill(columnWidth);
    });
  }, [headers, columnWidth]);

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

  const widthFor = (idx) => colWidths[idx] ?? columnWidth;

  const cellStyle = useMemo(
    () => headers.map((_, i) => ({ minWidth: `${widthFor(i)}px`, width: `${widthFor(i)}px` })),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [headers, colWidths, columnWidth]
  );

  const startResize = (idx, event) => {
    event.preventDefault();
    const startX = event.clientX;
    const initial = widthFor(idx);

    const onMouseMove = (e) => {
      const delta = e.clientX - startX;
      const next = Math.max(160, initial + delta);
      setColWidths((prev) => {
        const base = prev.length === headers.length ? prev.slice() : new Array(headers.length).fill(columnWidth);
        base[idx] = next;
        return base;
      });
    };

    const onMouseUp = () => {
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseup", onMouseUp);
    };

    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseup", onMouseUp);
  };

  return (
    <div className="overflow-x-auto">
      <table className="border-collapse table-fixed">
        <colgroup>
          {cellStyle.map((style, idx) => (
            <col key={idx} style={style} />
          ))}
        </colgroup>
        <thead>
          <tr>
            {headers.map((h, i) => (
              <th
                key={i}
                className="text-left text-sm font-semibold bg-slate-50 border-b border-slate-200 px-3 py-2 cursor-pointer select-none relative"
                onClick={() => onHeaderClick(i)}
                aria-sort={sortCol === i ? (sortDir === "asc" ? "ascending" : "descending") : "none"}
                title="Click to sort"
                style={cellStyle[i]}
              >
                <span>{h}</span>
                <span className="inline-block ml-1 text-slate-400">{arrow(i)}</span>
                <span
                  className="absolute right-0 top-0 h-full w-2 cursor-col-resize select-none"
                  onMouseDown={(e) => startResize(i, e)}
                  role="presentation"
                />
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sortedRows.map((r, ri) => (
            <tr key={ri} className="hover:bg-slate-50">
              {r.map((c, ci) => (
                <td key={ci} className="text-sm border-b border-slate-100 px-3 py-2" style={cellStyle[ci]}>{c}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default NativeTable;
