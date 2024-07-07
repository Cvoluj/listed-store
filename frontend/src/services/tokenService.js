import axios from 'axios';

const HOST = process.env.REACT_APP_HOST;
const BACKEND_PORT = process.env.REACT_APP_BACKEND_PORT;
const API_URL = `http://${HOST}:${BACKEND_PORT}/api/`;

const refreshToken = async () => {
  const refreshToken = localStorage.getItem('refreshToken');
  const response = await axios.post(`${API_URL}token/refresh/`, { refresh: refreshToken });
  localStorage.setItem('accessToken', response.data.access);
  return response.data.access;
};

const getAccessToken = () => {
  return localStorage.getItem('accessToken');
};

export { refreshToken, getAccessToken };