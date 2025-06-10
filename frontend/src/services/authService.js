import axios from 'axios';

const API_URL = 'http://localhost:8000/api/auth/';

const register = async (username, email, password, firstName, lastName) => {
  return axios.post(API_URL + 'register/', {
    username,
    email,
    password,
    password2: password,
    first_name: firstName,
    last_name: lastName
  });
};

const login = async (username, password) => {
  const response = await axios.post(API_URL + 'login/', {
    username,
    password
  });
  
  if (response.data.access) {
    localStorage.setItem('accessToken', response.data.access);
    localStorage.setItem('refreshToken', response.data.refresh);
    localStorage.setItem('user', JSON.stringify(response.data.user));
  }
  
  return response.data;
};



const logout = () => {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  localStorage.removeItem('user');
};

const getCurrentUser = () => {
  return JSON.parse(localStorage.getItem('user'));
};

const refreshToken = async () => {
  const refreshToken = localStorage.getItem('refreshToken');
  
  if (!refreshToken) {
    return Promise.reject('No refresh token available');
  }
  
  try {
    const response = await axios.post(API_URL + 'token/refresh/', {
      refresh: refreshToken
    });
    
    localStorage.setItem('accessToken', response.data.access);
    return response.data;
  } catch (error) {
    logout();
    return Promise.reject(error);
  }
};

// Interceptor para renovar el token cuando expire
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        await refreshToken();
        originalRequest.headers['Authorization'] = 'Bearer ' + localStorage.getItem('accessToken');
        return axios(originalRequest);
      } catch (refreshError) {
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

// Interceptor para añadir el token a las peticiones
axios.interceptors.request.use(
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

const authService = {
  register,
  login,
  logout,
  getCurrentUser,
  refreshToken
};

export default authService;

