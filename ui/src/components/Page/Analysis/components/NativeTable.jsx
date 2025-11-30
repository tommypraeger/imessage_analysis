import { useMemo, useState, useEffect } from "react";

const cellToNumber = (text) => {
  const n = parseFloat(String(text).replace(/[%,\$,\s,]/g, ""));
  return Number.isNaN(n) ? null : n;
};

const NativeTable = ({ headers, rows, defaultSortCol = 1, columnWidth = 160, enableCellColors = true }) => {
  const [sortCol, setSortCol] = useState(defaultSortCol);
  const [sortDir, setSortDir] = useState("desc"); // default for numeric
  const [colWidths, setColWidths] = useState([]);
  const [columnOrder, setColumnOrder] = useState([]);
  const [dragColIdx, setDragColIdx] = useState(null);

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

  useEffect(() => {
    setColumnOrder(headers.map((_, i) => i));
    setDragColIdx(null);
    // reset sort to default when headers change
    setSortCol(defaultSortCol);
  }, [headers, defaultSortCol]);

  const sortedRows = useMemo(() => {
    const actualCol = columnOrder[sortCol] ?? columnOrder[0] ?? 0;
    const dir = sortDir === "asc" ? 1 : -1;
    const nums = rows.map((r) => cellToNumber(r?.[actualCol] ?? ""));
    const isNumeric = nums.every((v) => v !== null);
    const copy = rows.slice();
    copy.sort((a, b) => {
      const av = a?.[actualCol] ?? "";
      const bv = b?.[actualCol] ?? "";
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

  const colorFor = (val, colIdx) => {
    if (!enableCellColors || colIdx === 0 || typeof val !== "number" || Number.isNaN(val)) return undefined;
    if (val === 1) return undefined;
    const min = -0.1;
    const max = 0.3;
    const clamped = Math.max(min, Math.min(max, val));
    const t = (clamped - min) / (max - min); // map [min,max] -> [0,1]
    const r = Math.round((1 - t) * 255);
    const g = Math.round(t * 255);
    const alpha = 0.2;
    return `rgba(${r},${g},0,${alpha})`;
  };

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

  const handleDragStart = (orderIdx) => {
    setDragColIdx(orderIdx);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (orderIdx) => {
    if (dragColIdx === null) return;
    const newOrder = columnOrder.slice();
    const [moved] = newOrder.splice(dragColIdx, 1);
    newOrder.splice(orderIdx, 0, moved);
    setColumnOrder(newOrder);
    // keep sort targeting same original column
    const originalIndex = columnOrder[sortCol];
    const newSortIdx = newOrder.indexOf(originalIndex);
    setSortCol(newSortIdx === -1 ? 0 : newSortIdx);
    setDragColIdx(null);
  };

  const displayHeaders = columnOrder.map((i) => headers[i]);
  const displayColStyles = columnOrder.map((i) => cellStyle[i]);
  const displayRows = sortedRows.map((r) => columnOrder.map((i) => r[i]));

  return (
    <div className="overflow-x-auto">
      <table className="border-collapse table-fixed">
        <colgroup>
          {displayColStyles.map((style, idx) => (
            <col key={idx} style={style} />
          ))}
        </colgroup>
        <thead>
          <tr>
            {displayHeaders.map((h, orderIdx) => (
              <th
                key={orderIdx}
                className={`text-left text-sm font-semibold bg-slate-50 border-b border-slate-200 px-3 py-2 cursor-pointer select-none relative ${
                  orderIdx === 0 ? "sticky left-0 z-10 bg-slate-50" : ""
                }`}
                onClick={() => onHeaderClick(orderIdx)}
                onDragStart={() => handleDragStart(orderIdx)}
                onDragOver={handleDragOver}
                onDrop={() => handleDrop(orderIdx)}
                aria-sort={sortCol === orderIdx ? (sortDir === "asc" ? "ascending" : "descending") : "none"}
                title="Click to sort"
                style={displayColStyles[orderIdx]}
              >
                <span>{h}</span>
                <span className="inline-block ml-1 text-slate-400">{arrow(orderIdx)}</span>
                <span
                  className="absolute right-0 top-0 h-full w-2 cursor-col-resize select-none"
                  onMouseDown={(e) => startResize(orderIdx, e)}
                  role="presentation"
                />
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {displayRows.map((r, ri) => (
            <tr key={ri} className="hover:bg-slate-50">
              {r.map((c, ci) => {
                const isNameCol = ci === 0;
                const rawVal = typeof c === "string" ? Number(c) : c;
                const bg = !isNameCol ? colorFor(rawVal, ci) : undefined;
                return (
                  <td
                    key={ci}
                    className={`text-sm border-b border-slate-100 px-3 py-2 ${isNameCol ? "sticky left-0 bg-white z-10" : ""}`}
                    style={{ ...displayColStyles[ci], backgroundColor: bg }}
                  >
                    {c}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default NativeTable;
