import axios from 'axios';

// Define a URL base usando uma variável de ambiente.
// Em desenvolvimento local, use 'http://localhost:5001' (ou a porta correta do seu backend local).
// No Render, defina a variável de ambiente REACT_APP_BACKEND_URL com a URL pública do seu backend.
const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5001'; // Use a porta correta do seu backend local se for diferente de 5001

const api = axios.create({
  baseURL: `${API_BASE_URL}/api` // Adiciona '/api' se o seu backend tiver um prefixo
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
      // throw { // Removido: Expected an error object to be thrown
      //   response: {
      //     data: {
      //       error: 'Usuário ou senha inválidos'
      //     }
      //   }
      // };
      throw new Error('Usuário ou senha inválidos'); // Adicionado: Lança uma instância de Error
    }
  } catch (error) {
    console.error('Erro no login:', error);
    throw error;
  }
};

export default api;