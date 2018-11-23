import { DEV_BASE_URL } from './dev.env';

let baseUrl;
if (process.env.NODE_ENV !== 'production') {
  baseUrl = DEV_BASE_URL;
} else {
  baseUrl = location.origin;
}

export const BASE_URL = baseUrl;
export const API_VERSION = '/api/v1';
export const BASE_API_URL = `${baseUrl}${API_VERSION}`;
