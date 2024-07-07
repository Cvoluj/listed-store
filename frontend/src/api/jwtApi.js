import axios from 'axios';

const HOST = process.env.REACT_APP_HOST;
const BACKEND_PORT = process.env.REACT_APP_BACKEND_PORT;
const API_URL = `http://${HOST}:${BACKEND_PORT}/api/`;

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const newToken = await refreshToken();
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + newToken;
      return api(originalRequest);
    }
    return Promise.reject(error);
  }
);

const refreshToken = async () => {
  const refreshToken = localStorage.getItem('refreshToken');
  const response = await axios.post(API_URL + 'auth/refresh/', { refresh: refreshToken });
  localStorage.setItem('accessToken', response.data.access);
  return response.data.access;
};

const jwtApi = api;
export default jwtApi;