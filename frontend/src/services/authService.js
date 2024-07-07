import axios from 'axios';

const HOST = process.env.REACT_APP_HOST;
const BACKEND_PORT = process.env.REACT_APP_BACKEND_PORT;
const API_URL = `http://${HOST}:${BACKEND_PORT}/api/`;

const register = (username, password, email, first_name, last_name) => {
  return axios.post(API_URL + 'register', {
    username,
    password,
    email,
    first_name,
    last_name,
  });
};

const login = (email, password) => {
  return axios.post(API_URL + 'auth/login/', {
    email,
    password,
  });
};

const logout = () => {
  localStorage.removeItem('user');
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
};

const getCurrentUser = () => {
  return JSON.parse(localStorage.getItem('user'));
};

const authService = {
  register,
  login,
  logout,
  getCurrentUser,
};

export default authService;
