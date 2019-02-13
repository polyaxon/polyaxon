import { Action } from 'redux';
import * as url from 'url';

import { BASE_API_URL } from '../constants/api';
import { getProjectUrl, getProjectUrlFromName, getUserUrl, handleAuthError } from '../constants/utils';
import history from '../history';
import { BookmarkModel } from '../models/bookmark';
import { ProjectModel } from '../models/project';
import { ARCHIVES, BOOKMARKS } from '../utils/endpointList';

export enum actionTypes {
  CREATE_PROJECT = 'CREATE_PROJECT',
  DELETE_PROJECT = 'DELETE_PROJECT',
  UPDATE_PROJECT = 'UPDATE_PROJECT',
  ARCHIVE_PROJECT = 'ARCHIVE_PROJECT',
  RESTORE_PROJECT = 'RESTORE_PROJECT',
  RECEIVE_PROJECT = 'RECEIVE_PROJECT',
  REQUEST_PROJECT = 'REQUEST_PROJECT',
  RECEIVE_PROJECTS = 'RECEIVE_PROJECTS',
  REQUEST_PROJECTS = 'REQUEST_PROJECTS',
  BOOKMARK_PROJECT = 'BOOKMARK_PROJECT',
  UNBOOKMARK_PROJECT = 'UNBOOKMARK_PROJECT',
  START_PROJECT_NOTEBOOK = 'START_PROJECT_NOTEBOOK',
  STOP_PROJECT_NOTEBOOK = 'STOP_PROJECT_NOTEBOOK',
  START_PROJECT_TENSORBOARD = 'START_PROJECT_TENSORBOARD',
  STOP_PROJECT_TENSORBOARD = 'STOP_PROJECT_TENSORBOARD'
}

export interface CreateUpdateReceiveProjectAction extends Action {
  type: actionTypes.CREATE_PROJECT | actionTypes.UPDATE_PROJECT | actionTypes.RECEIVE_PROJECT;
  project: ProjectModel;
}

export interface DeleteProjectAction extends Action {
  type: actionTypes.DELETE_PROJECT;
  projectName: string;
}

export interface RestoreProjectAction extends Action {
  type: actionTypes.RESTORE_PROJECT;
  projectName: string;
}

export interface ArchiveProjectAction extends Action {
  type: actionTypes.ARCHIVE_PROJECT;
  projectName: string;
}

export interface ReceiveProjectsAction extends Action {
  type: actionTypes.RECEIVE_PROJECTS;
  projects: ProjectModel[];
  count: number;
}

export interface RequestProjectsAction extends Action {
  type: actionTypes.REQUEST_PROJECTS | actionTypes.REQUEST_PROJECT;
}

export interface BookmarkProjectAction extends Action {
  type: actionTypes.BOOKMARK_PROJECT | actionTypes.UNBOOKMARK_PROJECT;
  projectName: string;
}

export interface ProjectNotebookAction extends Action {
  type: actionTypes.START_PROJECT_NOTEBOOK | actionTypes.STOP_PROJECT_NOTEBOOK;
  projectName: string;
}

export interface ProjectTensorboardAction extends Action {
  type: actionTypes.START_PROJECT_TENSORBOARD | actionTypes.STOP_PROJECT_TENSORBOARD;
  projectName: string;
}

export type ProjectAction =
  CreateUpdateReceiveProjectAction
  | DeleteProjectAction
  | ArchiveProjectAction
  | RestoreProjectAction
  | ReceiveProjectsAction
  | RequestProjectsAction
  | BookmarkProjectAction
  | ProjectNotebookAction
  | ProjectTensorboardAction;

export function createProjectActionCreator(project: ProjectModel): CreateUpdateReceiveProjectAction {
  return {
    type: actionTypes.CREATE_PROJECT,
    project
  };
}

export function deleteProjectActionCreator(projectName: string): DeleteProjectAction {
  return {
    type: actionTypes.DELETE_PROJECT,
    projectName
  };
}

export function archiveProjectActionCreator(projectName: string): ArchiveProjectAction {
  return {
    type: actionTypes.ARCHIVE_PROJECT,
    projectName
  };
}

export function restoreProjectActionCreator(projectName: string): RestoreProjectAction {
  return {
    type: actionTypes.RESTORE_PROJECT,
    projectName
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

export function receiveBookmarkedProjectsActionCreator(bookmarkedProjects: BookmarkModel[],
                                                       count: number): ReceiveProjectsAction {
  const projects: ProjectModel[] = [];
  for (const bookmarkedProject of bookmarkedProjects) {
    projects.push(bookmarkedProject.content_object as ProjectModel);
  }
  return {
    type: actionTypes.RECEIVE_PROJECTS,
    projects,
    count,
  };
}

export function bookmarkProjectActionCreator(projectName: string) {
  return {
    type: actionTypes.BOOKMARK_PROJECT,
    projectName,
  };
}

export function unbookmarkProjectActionCreator(projectName: string) {
  return {
    type: actionTypes.UNBOOKMARK_PROJECT,
    projectName,
  };
}

export function startProjectNotebookActionCreator(projectName: string): ProjectNotebookAction {
  return {
    type: actionTypes.START_PROJECT_NOTEBOOK,
    projectName
  };
}

export function stopProjectNotebookActionCreator(projectName: string): ProjectNotebookAction {
  return {
    type: actionTypes.STOP_PROJECT_NOTEBOOK,
    projectName
  };
}

export function startProjectTensorboardActionCreator(projectName: string): ProjectTensorboardAction {
  return {
    type: actionTypes.START_PROJECT_TENSORBOARD,
    projectName
  };
}

export function stopProjectTensorboardActionCreator(projectName: string): ProjectTensorboardAction {
  return {
    type: actionTypes.STOP_PROJECT_TENSORBOARD,
    projectName
  };
}

export function createProject(user: string, project: ProjectModel): any {
  return (dispatch: any, getState: any) => {
    // FIX ME: We need to add a first dispatch here so we show it to the user before
    // sending it to the backend: dispatch(createProjectActionCreator(project))
    return fetch(`${BASE_API_URL}/${user}`, {
      method: 'POST',
      body: JSON.stringify(project),
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.json())
      .then((json) => dispatch(receiveProjectActionCreator(json)));
  };
}

export function updateProject(projectName: string, updateDict: { [key: string]: any }): any {
  return (dispatch: any, getState: any) => {
    const projectUrl = getProjectUrlFromName(projectName, false);
    return fetch(`${BASE_API_URL}/${projectUrl}`, {
      method: 'PATCH',
      body: JSON.stringify(updateDict),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.json())
      .then((json) => dispatch(updateProjectActionCreator(json)));
  };
}

export function deleteProject(projectName: string, redirect: boolean = false): any {
  const projectUrl = getProjectUrlFromName(projectName, false);
  return (dispatch: any, getState: any) => {
    return fetch(`${BASE_API_URL}${projectUrl}`, {
      method: 'DELETE',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => {
        const dispatched = dispatch(deleteProjectActionCreator(projectName));
        if (redirect) {
          const values = projectName.split('.');
          history.push(getUserUrl(values[0], true));
        }
        return dispatched;
      });
  };
}

export function archiveProject(projectName: string, redirect: boolean = false): any {
  const projectUrl = getProjectUrlFromName(projectName, false);
  return (dispatch: any, getState: any) => {
    return fetch(`${BASE_API_URL}${projectUrl}/archive`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => {
        const dispatched = dispatch(archiveProjectActionCreator(projectName));
        if (redirect) {
          const values = projectName.split('.');
          history.push(getUserUrl(values[0], true));
        }
        return dispatched;
      });
  };
}

export function restoreProject(projectName: string): any {
  const projectUrl = getProjectUrlFromName(projectName, false);
  return (dispatch: any, getState: any) => {
    return fetch(`${BASE_API_URL}${projectUrl}/restore`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(restoreProjectActionCreator(projectName)));
  };
}

function _fetchProjects(projectsUrl: string,
                        endpointList: string,
                        filters: { [key: string]: number | boolean | string } = {},
                        dispatch: any,
                        getState: any): any {
  dispatch(requestProjectsActionCreator());
  const urlPieces = location.hash.split('?');
  const baseUrl = urlPieces[0];
  if (Object.keys(filters).length) {
    projectsUrl += url.format({query: filters});
    if (baseUrl) {
      history.push(baseUrl + url.format({query: filters}));
    }
  } else if (urlPieces.length > 1) {
    history.push(baseUrl);
  }

  const dispatchActionCreator = (results: any, count: number) => {
    if (endpointList === BOOKMARKS) {
      return dispatch(receiveBookmarkedProjectsActionCreator(results, count));
    } else {
      return dispatch(receiveProjectsActionCreator(results, count));
    }
  };

  return fetch(projectsUrl, {
    headers: {
      Authorization: 'token ' + getState().auth.token
    }
  })
    .then((response) => handleAuthError(response, dispatch))
    .then((response) => response.json())
    .then((json) => dispatchActionCreator(json.results, json.count))
    .catch((error) => undefined);
}

export function fetchBookmarkedProjects(user: string,
                                        filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const projectsUrl = `${BASE_API_URL}/bookmarks/${user}/projects`;
    return _fetchProjects(projectsUrl, BOOKMARKS, filters, dispatch, getState);
  };
}

export function fetchArchivedProjects(user: string,
                                      filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const projectsUrl = `${BASE_API_URL}/archives/${user}/projects`;
    return _fetchProjects(projectsUrl, ARCHIVES, filters, dispatch, getState);
  };
}

export function fetchProjects(user: string,
                              filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const projectsUrl = `${BASE_API_URL}/${user}`;

    return _fetchProjects(projectsUrl, '', filters, dispatch, getState);
  };
}

export function fetchProject(user: string, projectName: string): any {
  const projectUrl = getProjectUrl(user, projectName, false);
  return (dispatch: any, getState: any) => {
    dispatch(requestProjectActionCreator());
    return fetch(`${BASE_API_URL}${projectUrl}`, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.json())
      .then((json) => dispatch(receiveProjectActionCreator(json)));
  };
}

export function bookmark(projectName: string): any {
  const projectUrl = getProjectUrlFromName(projectName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${projectUrl}/bookmark`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(bookmarkProjectActionCreator(projectName)));
  };
}

export function unbookmark(projectName: string): any {
  const projectUrl = getProjectUrlFromName(projectName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${projectUrl}/unbookmark`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(unbookmarkProjectActionCreator(projectName)));
  };
}

export function startNotebook(projectName: string): any {
  const projectUrl = getProjectUrlFromName(projectName, false);
  return (dispatch: any, getState: any) => {
    return fetch(`${BASE_API_URL}${projectUrl}/notebook/start`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => {
        return dispatch(startProjectNotebookActionCreator(projectName));
      });
  };
}

export function stopNotebook(projectName: string): any {
  const projectUrl = getProjectUrlFromName(projectName, false);
  return (dispatch: any, getState: any) => {
    return fetch(`${BASE_API_URL}${projectUrl}/notebook/stop`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => {
        return dispatch(stopProjectNotebookActionCreator(projectName));
      });
  };
}

export function startTensorboard(projectName: string): any {
  const projectUrl = getProjectUrlFromName(projectName, false);
  return (dispatch: any, getState: any) => {
    return fetch(`${BASE_API_URL}${projectUrl}/tensorboard/start`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => {
        return dispatch(startProjectTensorboardActionCreator(projectName));
      });
  };
}

export function stopTensorboard(projectName: string): any {
  const projectUrl = getProjectUrlFromName(projectName, false);
  return (dispatch: any, getState: any) => {
    return fetch(`${BASE_API_URL}${projectUrl}/tensorboard/stop`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => {
        return dispatch(stopProjectTensorboardActionCreator(projectName));
      });
  };
}
