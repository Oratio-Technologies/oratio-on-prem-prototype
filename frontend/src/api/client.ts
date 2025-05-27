// import { supabase } from '../lib/supabase';
// const baseURL = import.meta.env.VITE_API_HOST || 'https://docsapi.arc53.com';
const baseURL = 'http://127.0.0.1:8000';
// const baseURL ='http://inference-service.default.svc.cluster.local:8000/';
// const baseURL = 'http://9.141.184.18:8000';
// In your frontend API client configuration

// const baseURL = 'http://131.189.216.19:8000';
// const baseURL = 'https://chat.oratiotechnologies.com';
const defaultHeaders = {
  'Content-Type': 'application/json',
};

// const getAuthHeader = async (): Promise<HeadersInit> => {
//   const session = await supabase.auth.getSession();
//   return session.data.session?.access_token
//     ? { Authorization: `Bearer ${session.data.session.access_token}` }
//     : {};
// };

const apiClient = {
  get: async (
    url: string,
    headers = {},
    signal?: AbortSignal,
  ): Promise<any> => {
    return fetch(`${baseURL}${url}`, {
      method: 'GET',
      headers: {
        ...defaultHeaders,
        ...headers,
      },
      signal,
    }).then((response) => {
      return response;
    });
  },

  post: async (
    url: string,
    data: any,
    headers = {},
    signal?: AbortSignal,
  ): Promise<any> => {
    return fetch(`${baseURL}${url}`, {
      method: 'POST',
      headers: {
        ...defaultHeaders,
        ...headers,
      },
      body: JSON.stringify(data),
      signal,
    }).then((response) => {
      return response;
    });
  },

  put: async (
    url: string,
    data: any,
    headers = {},
    signal?: AbortSignal,
  ): Promise<any> => {
    return fetch(`${baseURL}${url}`, {
      method: 'PUT',
      headers: {
        ...defaultHeaders,
        ...headers,
      },
      body: JSON.stringify(data),
      signal,
    }).then((response) => {
      return response;
    });
  },

  delete: async (
    url: string,
    headers = {},
    signal?: AbortSignal,
  ): Promise<any> => {
    return fetch(`${baseURL}${url}`, {
      method: 'DELETE',
      headers: {
        ...defaultHeaders,
        ...headers,
      },
      signal,
    }).then((response) => {
      return response;
    });
  },
};

export default apiClient;
