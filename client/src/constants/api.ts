let baseUrl;
if (process.env.NODE_ENV !== 'production') {
  baseUrl = 'http://35.193.198.132/';
} else {
  baseUrl = location.origin;
}

export const BASE_URL = baseUrl;
export const BASE_API_URL = `${baseUrl}/api/v1`;
