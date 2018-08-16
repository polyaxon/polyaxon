import * as Raven from 'raven-js';
import { b64DecodeUnicode } from './libs/utils';

const configureRaven = () => {
  if (process.env.NODE_ENV === 'production') {
    const dns = 'aHR0cHM6Ly8zMmRiMzRlNDIzODI0Mzk1YWZhYjMwMjA5ODcyMzc5OUBzZW50cnkuaW8vMTI2MzQ4MA==';
    Raven.config(b64DecodeUnicode(dns)).install();
  }
};

export default configureRaven;
