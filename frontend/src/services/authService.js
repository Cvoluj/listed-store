import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const HOST = process.env.REACT_APP_HOST;
const BACKEND_PORT = process.env.REACT_APP_BACKEND_PORT;
const API_URL = `http://${HOST}:${BACKEND_PORT}/api/`;

const register = (username, password, email, first_name, last_name) => {
  alert(username + password + email + first_name + last_name)
  return axios.post(API_URL + 'auth/register/', {
    username,
    first_name,
    last_name,
    email,
    password,
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

const checkToken = () => {
  const accessToken = localStorage.getItem('accessToken');
  if (accessToken) {
    try {
      const decodedToken = jwtDecode(accessToken);
      const currentTime = Date.now() / 1000; // Convert milliseconds to seconds

      if (decodedToken.exp > currentTime) {
        const user = authService.getCurrentUser();
        return { isLoggedIn: true, user };
      }
    } catch (error) {
      console.error('Token decoding error:', error);
    }
  }
  return { isLoggedIn: false, user: null };
}

const authService = {
  register,
  login,
  logout,
  getCurrentUser,
  checkToken,
};

export default authService;
