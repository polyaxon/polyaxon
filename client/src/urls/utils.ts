import * as Cookies from 'js-cookie';

import { BASE_URL } from '../constants/api';

export const dateOptions = {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'};

export let urlifyProjectName = (projectName: string) => {
  // Replaces . by /
  const re = /\./gi;
  return projectName.replace(re, '\/');
};

export let splitUniqueName = (uniqueName: string) => {
  return uniqueName.split('.');
};

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

export let getCatalogUrl = (resourceType: string,
                            owner?: string,
                            app: boolean = true) => {
  let url = app ? '/app/catalogs' : '/catalogs';
  if (owner) {
    url = `${url}/${owner}`;
  }
  return `${url}/${resourceType}`;
};

export let getCatalogEntityUrl = (resourceType: string,
                                  name: string,
                                  owner?: string,
                                  app: boolean = true) => {
  const url = getCatalogUrl(resourceType, owner, app);
  return `${url}/${name}`;
};

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

export let getTensorboardApiUrlFromName = (uniqueName: string, app: boolean = true): string => {
  const values = uniqueName.split('.');
  return getTensorboardApiUrl(values[0], values[1], values[values.length - 1], app);
};

export let getNotebookApiUrlFromName = (uniqueName: string, app: boolean = true): string => {
  const values = uniqueName.split('.');
  return getNotebookApiUrl(values[0], values[1], values[values.length - 1], app);
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

export let getTensorboardApiUrl = (username: string,
                                   projectName: string,
                                   tensorboardId: number | string,
                                   app: boolean = true) => {
  const projectUrl = getProjectUrl(username, projectName, app);

  return `${projectUrl}/tensorboards/${tensorboardId}`;
};

export let getNotebookApiUrl = (username: string,
                                projectName: string,
                                notebookId: number | string,
                                app: boolean = true) => {
  const projectUrl = getProjectUrl(username, projectName, app);

  return `${projectUrl}/notebooks/${notebookId}`;
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

export let getTensorboardUniqueName = (username: string,
                                       projectName: string,
                                       buildId: number | string) => {
  const projectUrl = getProjectUniqueName(username, projectName);
  return `${projectUrl}.tensorboards.${buildId}`;
};

export let getNotebookUniqueName = (username: string,
                                    projectName: string,
                                    buildId: number | string) => {
  const projectUrl = getProjectUniqueName(username, projectName);
  return `${projectUrl}.notebooks.${buildId}`;
};

export function getGroupName(projectName: string, groupId: number | string) {
  return `${projectName}.${groupId}`;
}
