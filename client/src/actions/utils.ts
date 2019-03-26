import { fetchUser } from './user';

export const stdHandleError = (response: Response,
                               dispatch: any,
                               errorActionCreator: any,
                               notFoundError: string,
                               defaultError: string,
                               args?: any[]): any => {
  if (!response.ok) {
    if (response.status === 404) {
      dispatch(errorActionCreator(response.status, notFoundError, ...args || []));
    } else if (response.status === 400) {
      return Promise.reject({status: response.status, value: response});
    } else if (response.status === 401 || response.status === 403) {
      dispatch(fetchUser());
    } else {
      dispatch(errorActionCreator(response.status, defaultError, ...args || []));
    }

    return Promise.reject({status: response.status, value: response.statusText});
  }
  return response;
};

export const stdFetchHandleError = (response: Response,
                                    dispatch: any,
                                    errorActionCreator: any,
                                    notFoundError: string,
                                    defaultError: string,
                                    args?: any[]): any => {
  if (!response.ok) {
    if (response.status === 404) {
      dispatch(errorActionCreator(response.status, notFoundError, ...args || []));
    } else if (response.status === 400) {
      return Promise.reject({status: response.status, value: response});
    } else if (response.status === 401 || response.status === 403) {
      dispatch(fetchUser());
    } else {
      dispatch(errorActionCreator(response.status, defaultError, ...args || []));
    }

    return Promise.reject({status: response.status, value: response.statusText});
  }
  return response;
};

export const stdCreateHandleError = (response: Response,
                                     dispatch: any,
                                     errorActionCreator: any,
                                     notFoundError: string,
                                     defaultError: string,
                                     args?: any[]): any => {
  if (!response.ok) {
    if (response.status === 404) {
      dispatch(errorActionCreator(response.status, notFoundError, ...args || []));
    } else if (response.status === 400) {
      return Promise.reject({status: response.status, value: response});
    } else if (response.status === 401 || response.status === 403) {
      dispatch(fetchUser());
    } else {
      dispatch(errorActionCreator(response.status, defaultError, ...args || []));
    }

    return Promise.reject({status: response.status, value: response.statusText});
  }
  return response;
};

export const stdDeleteHandleError = (response: Response,
                                     dispatch: any,
                                     errorActionCreator: any,
                                     notFoundError: string,
                                     defaultError: string,
                                     args?: any[]): any => {
  if (!response.ok) {
    if (response.status === 404) {
      dispatch(errorActionCreator(response.status, notFoundError, ...args || []));
    } else if (response.status === 401 || response.status === 403) {
      dispatch(fetchUser());
    } else {
      dispatch(errorActionCreator(response.status, defaultError, ...args || []));
    }

    return Promise.reject(response.statusText);
  }
  return response;
};
