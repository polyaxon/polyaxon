let baseUrl;
if (process.env.NODE_ENV !== 'production') {
  baseUrl = 'http://localhost:8000/api/v1';
} else {
  baseUrl = location.origin + '/api/v1';
}

export const BASE_URL = baseUrl;
