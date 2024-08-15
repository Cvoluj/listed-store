import React, { useState, useEffect } from 'react';
import { jwtDecode } from 'jwt-decode';
import { useNavigate } from 'react-router-dom';
import authService from '../services/authService';

const SignIn = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const checkToken = () => {
      const accessToken = localStorage.getItem('accessToken');
      if (accessToken) {
        try {
          const decodedToken = jwtDecode(accessToken);
          const currentTime = Date.now() / 10000; 

          if (decodedToken.exp > currentTime) {
            const user = authService.getCurrentUser();
            setMessage(`Hey, ${user.username}, you are already logged in`);
            setIsLoggedIn(true);
          } else {
            setIsLoggedIn(false);
          }
        } catch (error) {
          console.error('Token decoding error:', error);
          setIsLoggedIn(false);
        }
      } else {
        setIsLoggedIn(false);
      }
    };

    checkToken();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await authService.login(email, password);
      localStorage.setItem('user', JSON.stringify(response.data));
      localStorage.setItem('accessToken', response.data.access);
      localStorage.setItem('refreshToken', response.data.refresh);
      navigate('/'); // Redirect to home or user dashboard
    } catch (err) {
      setError('Invalid username or password');
    }
  };

  return (
    <div className="container mt-5">
      {isLoggedIn ? (
        <div>
          <h2>Logged In</h2>
          <div className="form-group">
            <label>{message}</label>
          </div>
        </div>
      ) : (
        <div>
          <h2>Sign In</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Email</label>
              <input
                type="text"
                className="form-control"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                className="form-control"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            {error && <div className="alert alert-danger">{error}</div>}
            <button type="submit" className="btn btn-primary">Sign In</button>
          </form>
        </div>
      )}
    </div>
  );
};

export default SignIn;