import * as Raven from '@sentry/browser';
import { b64DecodeUnicode } from './constants/utils';

const configureRaven = () => {
  if (process.env.NODE_ENV === 'staging') {
    const dsn = 'aHR0cHM6Ly85NTZmODkwNDdhYTk0ZGQ1ODU4Mjg0N2E5YjVjMzliZEBzZW50cnkuaW8vMTE5NzU5OA==';
    Raven.init({ dsn: b64DecodeUnicode(dsn) });
  }
};

export default configureRaven;
