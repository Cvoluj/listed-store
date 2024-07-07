import React from 'react';
import { Route, Routes } from 'react-router-dom';
import Content from './components/Base/Content';
import UserPage from './components/User/UserPage';
import SignInPage from './pages/SignInPage';
// import SignUpPage from './pages/SignUpPage';


const App = () => {
  return (
    <Routes>
        <Route path="/signin" element={<SignInPage />} />
        {/* <Route path="/signup" element={<SignUpPage />} /> */}
        <Route path="/" element={<Content />} />
        <Route path="/user/:publicId" element={<UserPage />} />
    </Routes>
  );
};

export default App;