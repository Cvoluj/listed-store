// src/context/AuthContext.js
import React, { createContext, useState, useEffect } from 'react';
import { login, register, refreshToken } from '../api/auth';

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(() => 
    JSON.parse(localStorage.getItem('authTokens')) || null
  );
  const [user, setUser] = useState(() => 
    JSON.parse(localStorage.getItem('user')) || null
  );

  useEffect(() => {
    if (authTokens) {
      const interval = setInterval(() => {
        refreshToken(authTokens.refresh).then(data => {
          setAuthTokens(data);
          localStorage.setItem('authTokens', JSON.stringify(data));
        });
      }, 15 * 60 * 1000); // Auto-refresh every 15 minutes

      return () => clearInterval(interval);
    }
  }, [authTokens]);

  const handleLogin = async (credentials) => {
    const data = await login(credentials);
    setAuthTokens(data);
    setUser(data.user);
    localStorage.setItem('authTokens', JSON.stringify(data));
    localStorage.setItem('user', JSON.stringify(data.user));
  };

  const handleRegister = async (data) => {
    await register(data);
  };

  const handleLogout = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem('authTokens');
    localStorage.removeItem('user');
  };

  return (
    <AuthContext.Provider value={{ authTokens, user, handleLogin, handleRegister, handleLogout }}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthProvider, AuthContext };
