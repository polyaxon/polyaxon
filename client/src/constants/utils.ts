import * as Cookies from 'js-cookie';
import * as _ from 'lodash';
import * as moment from 'moment';

import { fetchUser } from '../actions/user';
import { BASE_URL } from '../constants/api';
import { TokenStateSchema } from '../models/token';

export const dateOptions = {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'};

export let urlifyProjectName = (projectName: string) => {
  // Replaces . by /
  const re = /\./gi;
  return projectName.replace(re, '\/');
};

export let splitUniqueName = (uniqueName: string) => {
  return uniqueName.split('.');
};

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

export let getHomeUrl = () => {
  const user = Cookies.get('user');
  return `/app/${user}/`;
};

export let getLoginUrl = (external?: boolean): string => {
  external = external || false;
  const loginUrl = '/users/login/';
  return external ? `${BASE_URL}${loginUrl}` : loginUrl;
};

export let getLogoutUrl = () => `/users/logout/`;

export let getUserUrl = (username: string, app: boolean = true) => {
  return app ? `/app/${username}` : `/${username}`;
};

export let getProjectUrl = (username: string, projectName: string, app: boolean = true) => {
  return `${getUserUrl(username, app)}/${projectName}`;
};

export let getBookmarksUrl = (username: string) => `/app/bookmarks/${username}`;
export let getArchivesUrl = (username: string) => `/app/archives/${username}`;

export let getProjectTensorboardUrl = (projectName: string) => {
  const values = splitUniqueName(projectName);
  return `/tensorboard/${values[0]}/${values[1]}/`;
};

export let getExperimentTensorboardUrl = (projectName: string, experimentId: string | number) => {
  const values = splitUniqueName(projectName);
  return `/tensorboard/${values[0]}/${values[1]}/experiments/${experimentId}/`;
};

export let getGroupTensorboardUrl = (projectName: string, groupId: string | number) => {
  const values = splitUniqueName(projectName);
  return `/tensorboard/${values[0]}/${values[1]}/groups/${groupId}/`;
};

export let getNotebookUrl = (projectName: string) => {
  const values = splitUniqueName(projectName);
  return `/notebook/${values[0]}/${values[1]}/`;
};

export let getProjectUniqueName = (username: string, projectName: string) => {
  return `${username}.${projectName}`;
};

export let getGroupUrl = (username: string,
                          projectName: string,
                          groupId: number | string,
                          app: boolean = true) => {
  const projectUrl = getProjectUrl(username, projectName, app);
  return `${projectUrl}/groups/${groupId}`;
};

export let getSelectionUrl = (username: string,
                              projectName: string,
                              groupId: number | string,
                              app: boolean = true) => {
  const projectUrl = getProjectUrl(username, projectName, app);
  return `${projectUrl}/selections/${groupId}`;
};


export let getGroupUniqueName = (username: string,
                                 projectName: string,
                                 groupId: number | string) => {
  const projectUniqueName = getProjectUniqueName(username, projectName);
  return `${projectUniqueName}.${groupId}`;
};

export let getExperimentUrl = (username: string,
                               projectName: string,
                               experimentId: number | string,
                               app: boolean = true) => {
  const projectUrl = getProjectUrl(username, projectName, app);
  return `${projectUrl}/experiments/${experimentId}`;
};

export let getExperimentUniqueName = (username: string,
                                      projectName: string,
                                      experimentId: number | string) => {
  const projectUniqueName = getProjectUniqueName(username, projectName);
  return `${projectUniqueName}.${experimentId}`;
};

export let getExperimentUrlFromName = (uniqueName: string, app: boolean = true): string => {
  const values = uniqueName.split('.');
  return getExperimentUrl(values[0], values[1], values[values.length - 1], app);
};

export let getProjectUrlFromName = (uniqueName: string, app: boolean = true): string => {
  const values = uniqueName.split('.');
  return getProjectUrl(values[0], values[1], app);
};

export let getBuildUrlFromName = (uniqueName: string, app: boolean = true): string => {
  const values = uniqueName.split('.');
  return getBuildUrl(values[0], values[1], values[values.length - 1], app);
};

export let getGroupUrlFromName = (uniqueName: string, app: boolean = true): string => {
  const values = uniqueName.split('.');
  return getGroupUrl(values[0], values[1], values[values.length - 1], app);
};

export let getSelectionUrlFromName = (uniqueName: string, app: boolean = true): string => {
  const values = uniqueName.split('.');
  return getSelectionUrl(values[0], values[1], values[values.length - 1], app);
};

export let getProjectNameFromUniqueName = (uniqueName: string) => {
  const values = uniqueName.split('.');
  return `${values[0]}.${values[1]}`;
};

export let getJobUrlFromName = (uniqueName: string, app: boolean = true): string => {
  const values = uniqueName.split('.');
  return getJobUrl(values[0], values[1], values[values.length - 1], app);
};

export let getJobUrl = (username: string,
                        projectName: string,
                        jobId: number | string,
                        app: boolean = true) => {
  const projectUrl = getProjectUrl(username, projectName, app);

  return `${projectUrl}/jobs/${jobId}`;
};

export let getBuildUrl = (username: string,
                          projectName: string,
                          buildId: number | string,
                          app: boolean = true) => {
  const projectUrl = getProjectUrl(username, projectName, app);

  return `${projectUrl}/builds/${buildId}`;
};

export let getExperimentJobUrl = (username: string,
                                  projectName: string,
                                  experimentId: number,
                                  jobId: number,
                                  app: boolean = true) => {
  const experimentUrl = getExperimentUrl(username, projectName, experimentId, app);

  return `${experimentUrl}/jobs/${jobId}`;
};

export let getExperimentJobUniqueName = (username: string,
                                         projectName: string,
                                         experimentId: number,
                                         jobId: number) => {
  const experimentUrl = getExperimentUniqueName(username, projectName, experimentId);
  return `${experimentUrl}.${jobId}`;
};

export let getJobUniqueName = (username: string,
                               projectName: string,
                               jobId: number | string) => {
  const projectUrl = getProjectUniqueName(username, projectName);
  return `${projectUrl}.jobs.${jobId}`;
};

export let getBuildUniqueName = (username: string,
                                 projectName: string,
                                 buildId: number | string) => {
  const projectUrl = getProjectUniqueName(username, projectName);
  return `${projectUrl}.builds.${buildId}`;
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

export function humanizeTimeDelta(startDate: string | Date, endtDate: string | Date): string | null {
  if (startDate == null || endtDate == null) {
    return null;
  }

  let seconds = moment(endtDate).diff(moment(startDate), 'seconds');
  let minutes = moment(endtDate).diff(moment(startDate), 'minutes');
  let hours = moment(endtDate).diff(moment(startDate), 'hours');
  const days = moment(endtDate).diff(moment(startDate), 'days');

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
