import React from 'react';
import { Route, Routes } from 'react-router-dom';
import Content from './components/Base/Content';
import UserPage from './components/User/UserPage';

const App = () => {
  return (
    <Routes>
        <Route path="/" element={<Content />} />
        <Route path="/user/:publicId" element={<UserPage />} />
    </Routes>
  );
};

export default App;