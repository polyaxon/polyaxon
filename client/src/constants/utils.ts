import * as Cookies from 'js-cookie';
import * as moment from 'moment';

import {TokenStateSchema} from '../models/token';
import {fetchUser} from '../actions/user';
import {BASE_URL} from '../constants/api';

export const dateOptions = {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'};

export let urlifyProjectName = function (projectName: string) {
  // Replaces . by /
  let re = /\./gi;
  return projectName.replace(re, '\/');
};

export let splitProjectName = function (projectName: string) {
  return projectName.split('.');
};

export let splitGroupName = function (groupName: string) {
  return groupName.split('.');
};

export let sortByUpdatedAt = function (a: any, b: any): any {
  let dateB: any = new Date(b.updated_at);
  let dateA: any = new Date(a.updated_at);
  return dateB - dateA;
};

export let pluralize = function (name: string, numObjects: number): string {
  if (numObjects !== 1) {
    return name + 's';
  }
  return name;
};

export let getToken = function (): TokenStateSchema | null {
  let user = Cookies.get('user');
  let token = Cookies.get('token');
  if (user !== undefined && token !== undefined) {
    return {token: token, user: user};
  }
  return null;
};

export let isUserAuthenticated = function () {
  return getToken() !== null;
};

export let getHomeUrl = function () {
  let user = Cookies.get('user');
  return `/app/${user}/`;
};

export let getLoginUrl = function (external?: boolean) {
  external = external || false;
  let loginUrl = '/users/login/';
  return external ? `${BASE_URL}${loginUrl}` : loginUrl;
};

export let getLogoutUrl = function () {
  return `/users/logout/`;
};

export let getUserUrl = function (username: string) {
  return `/app/${username}`;
};

export let getProjectUrl = function (username: string, projectName: string) {
  return `/app/${username}/${projectName}`;
};

export let getTensorboardUrl = function (username: string, projectName: string) {
  return `/tensorboard/${username}/${projectName}/`;
};

export let getNotebookUrl = function (username: string, projectName: string) {
  return `/notebook/${username}/${projectName}/`;
};

export let getProjectUniqueName = function (username: string, projectName: string) {
  return `${username}.${projectName}`;
};

export let getGroupUrl = function (username: string, projectName: string, groupId: number) {
  let projectUrl = getProjectUrl(username, projectName);
  return `${projectUrl}/groups/${groupId}/`;
};

export let getGroupUniqueName = function (username: string, projectName: string, groupId: number) {
  let projectUniqueName = getProjectUniqueName(username, projectName);
  return `${projectUniqueName}.${groupId}`;
};

export let getExperimentUrl = function (username: string, projectName: string, experimentId: number) {
  let projectUrl = getProjectUrl(username, projectName);
  return `${projectUrl}/experiments/${experimentId}/`;
};

export let getExperimentUniqueName = function (username: string, projectName: string, experimentId: number) {
  let projectUniqueName = getProjectUniqueName(username, projectName);
  return `${projectUniqueName}.${experimentId}`;
};

export let getJobtUrl = function (username: string,
                                  projectName: string,
                                  jobId: number) {
  let projectUrl = getProjectUrl(username, projectName);

  return `${projectUrl}/jobs/${jobId}/`;
};

export let getExperimentJobtUrl = function (username: string,
                                            projectName: string,
                                            experimentId: number,
                                            jobId: number) {
  let experimentUrl = getExperimentUrl(username, projectName, experimentId);

  return `${experimentUrl}/jobs/${jobId}/`;
};

export let getExperimentJobUniqueName = function (username: string,
                                                  projectName: string,
                                                  experimentId: number,
                                                  jobId: number) {
  let experimentUrl = getExperimentUniqueName(username, projectName, experimentId);
  return `${experimentUrl}.${jobId}`;
};

export let getJobUniqueName = function (username: string,
                                        projectName: string,
                                        jobId: number) {
  let projectUrl = getProjectUniqueName(username, projectName);
  return `${projectUrl}.${jobId}`;
};

export function getGroupName(projectName: string, groupId: number | string) {
  return `${projectName}.${groupId}`;
}

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
export function getExperimentIndexName(uniqueName: string): string {
  let values = uniqueName.split('.');
  if (values.length === 4) {
    values.splice(2, 1);
  }
  return values.join('.');
}

/*
  Convert a job unique name to an index by ignoring the group if it exists on the unique name, and task type.
*/
export function getExperimentJobIndexName(uniqueName: string): string {
  let values = uniqueName.split('.');
  if (values.length === 6) {
    values.splice(2, 1);
  }
  values.splice(4, 1);
  return values.join('.');
}

export function humanizeTimeDelta(startDate: string | Date, endtDate: string | Date): string | null {
  if (startDate == null || endtDate == null) {
    return null;
  }

  let seconds = moment(endtDate).diff(moment(startDate), 'seconds');
  let minutes = moment(endtDate).diff(moment(startDate), 'minutes');
  let hours = moment(endtDate).diff(moment(startDate), 'hours');
  let days = moment(endtDate).diff(moment(startDate), 'days');

  hours = hours % 24;
  minutes = minutes % 60;
  seconds = seconds % 60;
  let result = '';

  if (days >= 1) {
    result += `${days}d`;
    if (hours >= 1) {
      result += ` ${hours}h`;
    }
    if (minutes >= 1) {
      result += ` ${minutes}m`;
    }
    return result;
  }

  if (hours >= 1) {
    result += `${hours}h`;
    if (hours >= 1) {
      result += ` ${minutes}m`;
    }
    return result;
  }

  if (minutes >= 1) {
    result = `${minutes}m`;
    if (seconds >= 1) {
      result += ` ${seconds}s`;
    }
    return result;
  }

  return `${seconds}s`;
}

export const delay = (ms?: number) => new Promise(resolve =>
  setTimeout(resolve, ms || 0)
);

export function b64DecodeUnicode(str: string) {
  // Going backwards: from bytestream, to percent-encoding, to original string.
  return decodeURIComponent(atob(str).split('').map(function (c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));
}
