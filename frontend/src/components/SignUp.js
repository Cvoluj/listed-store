import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import authService from '../services/authService';

const SignUp = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    email: '',
    first_name: '',
    last_name: '',
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const [message, setMessage] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  

  useEffect(() => {
    const { isLoggedIn, user } = authService.checkToken();
    if (isLoggedIn) {
      setMessage(`Hey, ${user.user.username}, you are already logged in`);
      setIsLoggedIn(true);
    } else {
      setIsLoggedIn(false);
    }
  }, []);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      await authService.register(
        formData.username,
        formData.password,
        formData.email,
        formData.first_name,
        formData.last_name
      ).then(async (response) => {
        if (response.status === 201) {
          try {
            // this part of code duplicates SignIn logic, so if there will one more usage of this tempalate
            // localStorage.setItem('user', JSON.stringify(response.data));
            // localStorage.setItem('accessToken', response.data.access);
            // localStorage.setItem('refreshToken', response.data.refresh);
            // will be moved to authService.login()
            const loginResponse = await authService.login(formData.email, formData.password);      
            localStorage.setItem('user', JSON.stringify(loginResponse.data));
            localStorage.setItem('accessToken', loginResponse.data.access);
            localStorage.setItem('refreshToken', loginResponse.data.refresh);

            navigate('/');

          } catch (err) {
            setError('Failed to login after registration')
          }
        }
      })
      
    } catch (err) {
      setError('Failed to register. Please try again.');
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
      ) : (<div>
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Username</label>
          <input
            type="text"
            className="form-control"
            name="username"
            value={formData.username}
            onChange={handleChange}
          />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            className="form-control"
            name="password"
            value={formData.password}
            onChange={handleChange}
          />
        </div>
        <div className="form-group">
          <label>Email</label>
          <input
            type="email"
            className="form-control"
            name="email"
            value={formData.email}
            onChange={handleChange}
          />
        </div>
        <div className="form-group">
          <label>First Name</label>
          <input
            type="text"
            className="form-control"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
          />
        </div>
        <div className="form-group">
          <label>Last Name</label>
          <input
            type="text"
            className="form-control"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
          />
        </div>
        {error && <div className="alert alert-danger">{error}</div>}
        <button type="submit" className="btn btn-primary">Sign Up</button>
      </form>
      </div>
    )}
    </div>
  );
};

export default SignUp;
