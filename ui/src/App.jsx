import { useState } from "react";
import "./App.css";
import NavBar from "./components/NavBar";
import Page from "./components/Page";

const App = () => {
  const urlParams = new URLSearchParams(window.location.search);
  const pageParam = urlParams.get("page") ? urlParams.get("page") : "contacts";
  const [page, setPage] = useState(pageParam);

  return (
    <div className="min-h-screen bg-white text-slate-900">
      <NavBar page={page} setPage={setPage} />
      <div className="max-w-screen-2xl mx-auto px-2 sm:px-6 py-6">
        <Page page={page} />
      </div>
    </div>
  );
};

export default App;
