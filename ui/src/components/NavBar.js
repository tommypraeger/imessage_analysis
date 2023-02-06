const NavBar = ({ page, setPage }) => {
  const pages = ["contacts", "analysis"];
  const urlParams = new URLSearchParams(window.location.search);

  return (
    <ul id="nav-bar">
      {pages.map((pageName) => (
        <li
          key={pageName}
          className={page === pageName ? "active" : ""}
          onClick={() => {
            setPage(pageName);
            urlParams.set("page", pageName);
            window.location.search = urlParams.toString();
          }}
        >
          {pageName.charAt(0).toUpperCase() + pageName.slice(1)}
        </li>
      ))}
    </ul>
  );
};

export default NavBar;
