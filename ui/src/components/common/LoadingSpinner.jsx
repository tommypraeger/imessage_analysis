const LoadingSpinner = ({ size = 64, className = "" }) => {
  const style = { width: size, height: size };
  return (
    <div
      className={`rounded-full border-4 border-slate-300 border-t-slate-900 animate-spin ${className}`}
      style={style}
      role="status"
      aria-label="Loading"
    />
  );
};

export default LoadingSpinner;

