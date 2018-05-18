let baseUrl;
if (process.env.NODE_ENV !== 'production') {
  baseUrl = 'http://localhost:8000';
} else {
  baseUrl = location.origin;
}

export const BASE_URL = baseUrl;
export const BASE_API_URL = `${baseUrl}/api/v1`;
