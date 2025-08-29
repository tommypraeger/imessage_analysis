import { useEffect, useMemo, useRef, useState } from "react";

// Reusable minimal dropdown with optional grouped options and hover descriptions
// Props:
// - value: current selected value (string)
// - onChange: (val) => void
// - options: [{ value, label, desc? }] OR omit when using groups
// - groups: [{ label, options: [{ value, label, desc? }] }]
// - placeholder: string
// - buttonClass: string (optional)
// - listClass: string (optional)
const SelectMenu = ({
  value,
  onChange,
  options,
  groups,
  placeholder = "Select",
  buttonClass = "w-full border border-slate-300 rounded px-3 py-3 text-sm text-left bg-white hover:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-300",
  listClass = "absolute z-10 mt-1 w-full bg-white border border-slate-200 rounded shadow-md max-h-96 overflow-auto",
}) => {
  const [open, setOpen] = useState(false);
  const [hoverKey, setHoverKey] = useState(null);
  const ref = useRef(null);

  useEffect(() => {
    const onDocClick = (e) => {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false);
    };
    document.addEventListener("mousedown", onDocClick);
    return () => document.removeEventListener("mousedown", onDocClick);
  }, []);

  const flat = useMemo(() => {
    if (Array.isArray(options) && options.length) return options;
    if (Array.isArray(groups) && groups.length) return groups.flatMap((g) => g.options || []);
    return [];
  }, [options, groups]);

  const current = useMemo(() => flat.find((o) => o.value === value), [flat, value]);

  const onSelect = (val) => {
    onChange && onChange(val);
    setOpen(false);
  };

  const renderOption = (opt) => (
    <div
      key={opt.value}
      role="option"
      aria-selected={opt.value === value}
      aria-disabled={opt.disabled ? true : undefined}
      className={`px-3 py-2 text-sm ${
        opt.disabled
          ? "opacity-50 cursor-not-allowed"
          : "cursor-pointer hover:bg-slate-50"
      } ${opt.value === value && !opt.disabled ? "bg-slate-50" : ""}`}
      onMouseEnter={() => !opt.disabled && setHoverKey(opt.value)}
      onMouseLeave={() => setHoverKey(null)}
      onClick={() => !opt.disabled && onSelect(opt.value)}
    >
      <div className="flex items-center justify-between">
        <span className="font-medium text-slate-800">{opt.label ?? String(opt.value)}</span>
      </div>
      {hoverKey === opt.value && opt.desc ? (
        <div className="mt-1 text-xs text-slate-500">{opt.desc}</div>
      ) : null}
    </div>
  );

  return (
    <div className="relative" ref={ref}>
      <button
        type="button"
        className={`${buttonClass} flex items-center justify-between`}
        onClick={() => setOpen((o) => !o)}
        aria-haspopup="listbox"
        aria-expanded={open}
      >
        <span>{current?.label ?? placeholder}</span>
        <svg
          className="ml-2 h-4 w-4 text-slate-500"
          viewBox="0 0 20 20"
          fill="currentColor"
          aria-hidden="true"
        >
          <path
            fillRule="evenodd"
            d="M5.23 7.21a.75.75 0 011.06.02L10 10.94l3.71-3.71a.75.75 0 111.06 1.06l-4.24 4.24a.75.75 0 01-1.06 0L5.21 8.29a.75.75 0 01.02-1.08z"
            clipRule="evenodd"
          />
        </svg>
      </button>
      {open && (
        <div role="listbox" className={listClass}>
          {groups && groups.length ? (
            groups.map((g) => (
              <div key={g.label} className="py-1">
                <div className="px-3 py-1 text-[11px] uppercase tracking-wide text-slate-400">{g.label}</div>
                {(g.options || []).map(renderOption)}
              </div>
            ))
          ) : (
            (options || []).map(renderOption)
          )}
        </div>
      )}
    </div>
  );
};

export default SelectMenu;
