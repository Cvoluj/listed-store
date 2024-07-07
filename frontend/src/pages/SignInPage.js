import React from 'react';
import SignIn from '../components/SignIn';
import Navbar from '../components/Base/Navbar';
import Footer from '../components/Base/Footer';

const SignInPage = () => {
  return (
    <div className="SignIn">
      <Navbar />
      <SignIn />
      <Footer />
    </div>
  );
};

export default SignInPage;
