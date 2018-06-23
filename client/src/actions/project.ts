import { Action } from 'redux';
import * as url from 'url';

import history from '../history';
import { ProjectModel } from '../models/project';
import { BASE_API_URL } from '../constants/api';
import { handleAuthError } from '../constants/utils';

export enum actionTypes {
  CREATE_PROJECT = 'CREATE_PROJECT',
  DELETE_PROJECT = 'DELETE_PROJECT',
  UPDATE_PROJECT = 'UPDATE_PROJECT',
  RECEIVE_PROJECT = 'RECEIVE_PROJECT',
  REQUEST_PROJECT = 'REQUEST_PROJECT',
  RECEIVE_PROJECTS = 'RECEIVE_PROJECTS',
  REQUEST_PROJECTS = 'REQUEST_PROJECTS',
}

export interface CreateUpdateReceiveProjectAction extends Action {
  type: actionTypes.CREATE_PROJECT | actionTypes.UPDATE_PROJECT | actionTypes.RECEIVE_PROJECT;
  project: ProjectModel;
}

export interface DeleteProjectAction extends Action {
  type: actionTypes.DELETE_PROJECT;
  project: ProjectModel;
}

export interface ReceiveProjectsAction extends Action {
  type: actionTypes.RECEIVE_PROJECTS;
  projects: ProjectModel[];
  count: number;
}

export interface RequestProjectsAction extends Action {
  type: actionTypes.REQUEST_PROJECTS | actionTypes.REQUEST_PROJECT;
}

export type ProjectAction =
  CreateUpdateReceiveProjectAction
  | DeleteProjectAction
  | ReceiveProjectsAction
  | RequestProjectsAction;

export function createProjectActionCreator(project: ProjectModel): CreateUpdateReceiveProjectAction {
  return {
    type: actionTypes.CREATE_PROJECT,
    project
  };
}

export function deleteProjectActionCreator(project: ProjectModel): DeleteProjectAction {
  return {
    type: actionTypes.DELETE_PROJECT,
    project
  };
}

export function updateProjectActionCreator(project: ProjectModel): CreateUpdateReceiveProjectAction {
  return {
    type: actionTypes.UPDATE_PROJECT,
    project
  };
}

export function requestProjectActionCreator(): RequestProjectsAction {
  return {
    type: actionTypes.REQUEST_PROJECT,
  };
}

export function requestProjectsActionCreator(): RequestProjectsAction {
  return {
    type: actionTypes.REQUEST_PROJECTS,
  };
}

export function receiveProjectActionCreator(project: ProjectModel): CreateUpdateReceiveProjectAction {
  return {
    type: actionTypes.RECEIVE_PROJECT,
    project
  };
}

export function receiveProjectsActionCreator(projects: ProjectModel[], count: number): ReceiveProjectsAction {
  return {
    type: actionTypes.RECEIVE_PROJECTS,
    projects,
    count,
  };
}

export function createProject(user: string, project: ProjectModel): any {
  return (dispatch: any, getState: any) => {
    // FIX ME: We need to add a first dispatch here so we show it to the user before
    // sending it to the backend: dispatch(createProjectActionCreator(project))
    return fetch(BASE_API_URL + `/${user}`, {
      method: 'POST',
      body: JSON.stringify(project),
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then(response => handleAuthError(response, dispatch))
      .then(response => response.json())
      .then(json => dispatch(receiveProjectActionCreator(json)));
  };
}

export function deleteProject(project: ProjectModel): any {
  return (dispatch: any, getState: any) => {
    dispatch(deleteProjectActionCreator(project));
    return fetch(BASE_API_URL + `/${project.user}` + `/${project.name}`, {
      method: 'DELETE',
      headers: {
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then(response => handleAuthError(response, dispatch))
      .then(() => dispatch(receiveProjectsActionCreator([], 0)));
  };
}

export function fetchProjects(user: string,
                              filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestProjectsActionCreator());
    let projectsUrl = BASE_API_URL + `/${user}`;
    if (filters) {
      projectsUrl += url.format({query: filters});
      let baseUrl = location.hash.split('?')[0];
      history.push(baseUrl + url.format({ query: filters }));
    }
    return fetch(projectsUrl, {
      headers: {
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then(response => handleAuthError(response, dispatch))
      .then(response => response.json())
      .then(json => dispatch(receiveProjectsActionCreator(json.results, json.count)))
      .catch(error => undefined);
  };
}

export function fetchProject(user: string, projectName: string): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestProjectActionCreator());
    return fetch(BASE_API_URL + `/${user}` + `/${projectName}`, {
      headers: {
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then(response => handleAuthError(response, dispatch))
      .then(response => response.json())
      .then(json => dispatch(receiveProjectActionCreator(json)));
  };
}
