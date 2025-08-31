const NavBar = ({ page, setPage }) => {
  const pages = ["contacts", "analysis"];
  const onClick = (name) => {
    setPage(name);
    // Update the URL query param without reloading the page
    const url = new URL(window.location.href);
    url.searchParams.set("page", name);
    window.history.replaceState(null, "", url.toString());
  };

  return (
    <nav className="bg-white border-b border-slate-200">
      <div className="max-w-6xl mx-auto px-4">
        <div className="h-12 flex items-center gap-2">
          {pages.map((name) => {
            const active = page === name;
            return (
              <button
                key={name}
                onClick={() => onClick(name)}
                className={
                  (active
                    ? "text-slate-900 border-b-2 border-slate-900"
                    : "text-slate-600 hover:text-slate-900") +
                  " px-2 py-1 transition-colors"
                }
              >
                {name.charAt(0).toUpperCase() + name.slice(1)}
              </button>
            );
          })}
        </div>
      </div>
    </nav>
  );
};

export default NavBar;
