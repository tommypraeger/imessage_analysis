import React, { useState } from 'react';
import './App.css';
import NavBar from './components/NavBar';
import Page from './components/Page';

const App = () => {
  const [page, setPage] = useState('home');


  return (
    <div className='App'>
      <NavBar page={page} setPage={setPage} />
      <Page page={page} />
    </div>
  );
}

export default App;
