const Tooltip = ({ text }) => (
  <span className="relative inline-block align-middle ml-2 group">
    <svg
      className="h-4 w-4 text-slate-500 hover:text-slate-700"
      viewBox="0 0 20 20"
      fill="currentColor"
      aria-hidden="true"
    >
      <path
        fillRule="evenodd"
        d="M10 18a8 8 0 100-16 8 8 0 000 16zm.75-10.5a.75.75 0 10-1.5 0v.01a.75.75 0 001.5 0V7.5zm-2.25 6a.75.75 0 01.75-.75h.5v-2a.75.75 0 011.5 0v2h.25a.75.75 0 010 1.5H9.25a.75.75 0 01-.75-.75z"
        clipRule="evenodd"
      />
    </svg>
    <span className="absolute z-50 hidden group-hover:block group-focus-within:block left-1/2 -translate-x-1/2 mt-2 w-80 whitespace-normal break-words rounded bg-slate-800 px-3 py-2 text-xs text-white shadow-lg">
      {text}
    </span>
  </span>
);

export default Tooltip;
