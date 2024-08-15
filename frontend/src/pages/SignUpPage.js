import React from 'react';
import SignUp from '../components/SignUp';
import Navbar from '../components/Base/Navbar';
import Footer from '../components/Base/Footer';

const SignUpPage = () => {
  return (
    <div className="SignIn">
      <Navbar />
      <SignUp />
      <Footer />
    </div>
  );
};

export default SignUpPage;