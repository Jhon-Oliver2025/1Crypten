import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api'
});

// Interceptor para adicionar o token em todas as requisições
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const login = async ({ username, password }) => {
  try {
    // Simulando uma chamada de API com as credenciais fixas
    if (username === 'admin' && password === '311101') {
      const response = {
        data: {
          user: {
            username: 'admin',
            name: 'Administrador'
          },
          access_token: 'fake-jwt-token'
        }
      };
      
      localStorage.setItem('token', response.data.access_token);
      return response;
    } else {
      throw {
        response: {
          data: {
            error: 'Usuário ou senha inválidos'
          }
        }
      };
    }
  } catch (error) {
    console.error('Erro no login:', error);
    throw error;
  }
};

export default api;