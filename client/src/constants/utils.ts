import * as Cookies from 'js-cookie';
import * as _ from 'lodash';
import * as moment from 'moment';

import { fetchUser } from '../actions/user';
import { TokenStateSchema } from '../models/token';

export const dateOptions = {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'};

export let sortByUpdatedAt = (a: any, b: any) => {
  const dateB: any = new Date(b.updated_at);
  const dateA: any = new Date(a.updated_at);
  return dateB - dateA;
};

export let pluralize = (name: string, numObjects: number): string => {
  if (numObjects !== 1) {
    return name + 's';
  }
  return name;
};

export let getToken = (): TokenStateSchema | null => {
  const user = Cookies.get('user');
  const token = Cookies.get('token');
  const csrftoken = Cookies.get('csrftoken');
  if (user !== undefined && token !== undefined) {
    return {token, user, csrftoken: csrftoken || ''};
  }
  return null;
};

export let isUserAuthenticated = () => getToken() !== null;

export function handleAuthError(response: any, dispatch: any) {
  if (!response.ok) {
    dispatch(fetchUser());
    return Promise.reject(response.statusText);
  }
  return response;
}

/*
  Convert an experiment unique name to an index by ignoring the group if it exists on the unique name.
*/
export function getExperimentIndexName(uniqueName: string, fromJob: boolean = false): string {
  const values = uniqueName.split('.');
  if (fromJob) {
    values.pop();
  }
  if (values.length === 4) {
    values.splice(2, 1);
  }
  return values.join('.');
}

/*
  Convert a job unique name to an index by ignoring the group if it exists on the unique name, and task type.
*/
export function getExperimentJobIndexName(uniqueName: string): string {
  const values = uniqueName.split('.');
  if (values.length === 6) {
    values.splice(2, 1);
  }
  values.splice(4, 1);
  return values.join('.');
}

export const delay = (ms?: number) => new Promise((resolve) =>
  setTimeout(resolve, ms || 0)
);

export function b64DecodeUnicode(str: string) {
  // Going backwards: from bytestream, to percent-encoding, to original string.
  return decodeURIComponent(atob(str).split('').map((c) => {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));
}

export function isTrue(value?: boolean) {
  return !_.isNil(value) && value;
}
