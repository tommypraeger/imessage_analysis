import React, { useState } from "react";
import "./App.css";
import NavBar from "./components/NavBar";
import Page from "./components/Page";

const App = () => {
  const urlParams = new URLSearchParams(window.location.search);
  const pageParam = urlParams.get("page") ? urlParams.get("page") : "contacts";
  const [page, setPage] = useState(pageParam);

  return (
    <div className="App">
      <NavBar page={page} setPage={setPage} />
      <Page page={page} />
    </div>
  );
};

export default App;
