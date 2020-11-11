const NavBar = ({ page, setPage }) => {
  const pages = [
    'contacts',
    'analysis'
  ];

  return (
    <ul id='nav-bar'>
      {pages.map(pageName => (
        <li
          key={pageName}
          className={page === pageName ? 'active' : ''}
          onClick={() => setPage(pageName)}
        >
          {pageName.charAt(0).toUpperCase() + pageName.slice(1)}
        </li>
      ))}
    </ul>
  );
};

export default NavBar;