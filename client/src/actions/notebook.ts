import { Action } from 'redux';
import * as url from 'url';

import { BASE_API_URL } from '../constants/api';
import {
  getNotebookApiUrl,
  getNotebookApiUrlFromName,
  getProjectUrl,
  handleAuthError,
  urlifyProjectName
} from '../constants/utils';
import history from '../history';
import { BookmarkModel } from '../models/bookmark';
import { NotebookModel } from '../models/notebook';
import { ARCHIVES, BOOKMARKS } from '../utils/endpointList';

export enum actionTypes {
  CREATE_NOTEBOOK = 'CREATE_NOTEBOOK',
  DELETE_NOTEBOOK = 'DELETE_NOTEBOOK',
  STOP_NOTEBOOK = 'STOP_NOTEBOOK',
  ARCHIVE_NOTEBOOK = 'ARCHIVE_NOTEBOOK',
  RESTORE_NOTEBOOK = 'RESTORE_NOTEBOOK',
  UPDATE_NOTEBOOK = 'UPDATE_NOTEBOOK',
  RECEIVE_NOTEBOOK = 'RECEIVE_NOTEBOOK',
  RECEIVE_NOTEBOOKS = 'RECEIVE_NOTEBOOKS',
  REQUEST_NOTEBOOK = 'REQUEST_NOTEBOOK',
  REQUEST_NOTEBOOKS = 'REQUEST_NOTEBOOKS',
  BOOKMARK_NOTEBOOK = 'BOOKMARK_NOTEBOOK',
  UNBOOKMARK_NOTEBOOK = 'UNBOOKMARK_NOTEBOOK',
}

export interface CreateUpdateReceiveNotebookAction extends Action {
  type: actionTypes.CREATE_NOTEBOOK | actionTypes.UPDATE_NOTEBOOK | actionTypes.RECEIVE_NOTEBOOK;
  notebook: NotebookModel;
}

export interface DeleteNotebookAction extends Action {
  type: actionTypes.DELETE_NOTEBOOK;
  notebookName: string;
}

export interface ArchiveNotebookAction extends Action {
  type: actionTypes.ARCHIVE_NOTEBOOK;
  notebookName: string;
}

export interface RestoreNotebookAction extends Action {
  type: actionTypes.RESTORE_NOTEBOOK;
  notebookName: string;
}

export interface StopNotebookAction extends Action {
  type: actionTypes.STOP_NOTEBOOK;
  notebookName: string;
}

export interface BookmarkNotebookAction extends Action {
  type: actionTypes.BOOKMARK_NOTEBOOK | actionTypes.UNBOOKMARK_NOTEBOOK;
  notebookName: string;
}

export interface ReceiveNotebooksAction extends Action {
  type: actionTypes.RECEIVE_NOTEBOOKS;
  notebooks: NotebookModel[];
  count: number;
}

export interface RequestNotebooksAction extends Action {
  type: actionTypes.REQUEST_NOTEBOOKS | actionTypes.REQUEST_NOTEBOOK;
}

export type NotebookAction =
  CreateUpdateReceiveNotebookAction
  | DeleteNotebookAction
  | StopNotebookAction
  | ArchiveNotebookAction
  | RestoreNotebookAction
  | ReceiveNotebooksAction
  | RequestNotebooksAction
  | BookmarkNotebookAction;

export function createNotebookActionCreator(notebook: NotebookModel): CreateUpdateReceiveNotebookAction {
  return {
    type: actionTypes.CREATE_NOTEBOOK,
    notebook
  };
}

export function updateNotebookActionCreator(notebook: NotebookModel): CreateUpdateReceiveNotebookAction {
  return {
    type: actionTypes.UPDATE_NOTEBOOK,
    notebook
  };
}

export function deleteNotebookActionCreator(notebookName: string): DeleteNotebookAction {
  return {
    type: actionTypes.DELETE_NOTEBOOK,
    notebookName
  };
}

export function stopNotebookActionCreator(notebookName: string): StopNotebookAction {
  return {
    type: actionTypes.STOP_NOTEBOOK,
    notebookName
  };
}

export function archiveNotebookActionCreator(notebookName: string): ArchiveNotebookAction {
  return {
    type: actionTypes.ARCHIVE_NOTEBOOK,
    notebookName
  };
}

export function restoreNotebookActionCreator(notebookName: string): RestoreNotebookAction {
  return {
    type: actionTypes.RESTORE_NOTEBOOK,
    notebookName
  };
}

export function requestNotebookActionCreator(): RequestNotebooksAction {
  return {
    type: actionTypes.REQUEST_NOTEBOOK,
  };
}

export function requestNotebooksActionCreator(): RequestNotebooksAction {
  return {
    type: actionTypes.REQUEST_NOTEBOOKS,
  };
}

export function receiveNotebookActionCreator(notebook: NotebookModel): CreateUpdateReceiveNotebookAction {
  return {
    type: actionTypes.RECEIVE_NOTEBOOK,
    notebook
  };
}

export function receiveNotebooksActionCreator(notebooks: NotebookModel[],
                                              count: number): ReceiveNotebooksAction {
  return {
    type: actionTypes.RECEIVE_NOTEBOOKS,
    notebooks,
    count
  };
}

export function receiveBookmarkedNotebooksActionCreator(bookmarkedNotebooks: BookmarkModel[],
                                                        count: number): ReceiveNotebooksAction {
  const notebooks: NotebookModel[] = [];
  for (const bookmarkedNotebook of bookmarkedNotebooks) {
    notebooks.push(bookmarkedNotebook.content_object as NotebookModel);
  }
  return {
    type: actionTypes.RECEIVE_NOTEBOOKS,
    notebooks,
    count
  };
}

export function bookmarkNotebookActionCreator(notebookName: string) {
  return {
    type: actionTypes.BOOKMARK_NOTEBOOK,
    notebookName,
  };
}

export function unbookmarkNotebookActionCreator(notebookName: string) {
  return {
    type: actionTypes.UNBOOKMARK_NOTEBOOK,
    notebookName,
  };
}

function _fetchNotebooks(notebooksUrl: string,
                         endpointList: string,
                         filters: { [key: string]: number | boolean | string } = {},
                         dispatch: any,
                         getState: any): any {
  dispatch(requestNotebooksActionCreator());
  const urlPieces = location.hash.split('?');
  const baseUrl = urlPieces[0];
  if (Object.keys(filters).length) {
    notebooksUrl += url.format({query: filters});
    if (baseUrl) {
      history.push(baseUrl + url.format({query: filters}));
    }
  } else if (urlPieces.length > 1) {
    history.push(baseUrl);
  }

  const dispatchActionCreator = (results: any, count: number) => {
    if (endpointList === BOOKMARKS) {
      dispatch(receiveBookmarkedNotebooksActionCreator(results, count));
    } else {
      dispatch(receiveNotebooksActionCreator(results, count));
    }
  };

  return fetch(
    notebooksUrl, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
    .then((response) => handleAuthError(response, dispatch))
    .then((response) => response.json())
    .then((json) => dispatchActionCreator(json.results, json.count));
}

export function fetchBookmarkedNotebooks(user: string,
                                         filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const notebooksUrl = `${BASE_API_URL}/bookmarks/${user}/notebooks/`;
    return _fetchNotebooks(notebooksUrl, BOOKMARKS, filters, dispatch, getState);
  };
}

export function fetchArchivedNotebooks(user: string,
                                       filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const notebooksUrl = `${BASE_API_URL}/archives/${user}/notebooks/`;
    return _fetchNotebooks(notebooksUrl, ARCHIVES, filters, dispatch, getState);
  };
}

export function fetchNotebooks(projectUniqueName: string,
                               filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const notebooksUrl = `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/notebooks`;
    return _fetchNotebooks(notebooksUrl, '', filters, dispatch, getState);
  };
}

export function fetchNotebook(user: string, projectName: string, notebookId: number | string): any {
  const notebookUrl = getNotebookApiUrl(user, projectName, notebookId, false);
  return (dispatch: any, getState: any) => {
    dispatch(requestNotebookActionCreator());
    return fetch(
      `${BASE_API_URL}${notebookUrl}`, {
        headers: {
          Authorization: 'token ' + getState().auth.token
        }
      })
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.json())
      .then((json) => dispatch(receiveNotebookActionCreator(json)));
  };
}

export function updateNotebook(notebookName: string, updateDict: { [key: string]: any }): any {
  const notebookUrl = getNotebookApiUrlFromName(notebookName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${notebookUrl}`, {
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
      .then((json) => dispatch(updateNotebookActionCreator(json)));
  };
}

export function deleteNotebook(notebookName: string, redirect: boolean = false): any {
  const notebookUrl = getNotebookApiUrlFromName(notebookName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${notebookUrl}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => {
        const dispatched = dispatch(deleteNotebookActionCreator(notebookName));
        if (redirect) {
          const values = notebookName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#notebooks');
        }
        return dispatched;
      });
  };
}

export function archiveNotebook(notebookName: string, redirect: boolean = false): any {
  const notebookUrl = getNotebookApiUrlFromName(notebookName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${notebookUrl}/archive`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => {
        const dispatched = dispatch(archiveNotebookActionCreator(notebookName));
        if (redirect) {
          const values = notebookName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#notebooks');
        }
        return dispatched;
      });
  };
}

export function restoreNotebook(notebookName: string): any {
  const notebookUrl = getNotebookApiUrlFromName(notebookName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${notebookUrl}/restore`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(restoreNotebookActionCreator(notebookName)));
  };
}

export function stopNotebook(notebookName: string): any {
  const notebookUrl = getNotebookApiUrlFromName(notebookName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${notebookUrl}/stop`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(stopNotebookActionCreator(notebookName)));
  };
}

export function bookmark(notebookName: string): any {
  const notebookUrl = getNotebookApiUrlFromName(notebookName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${notebookUrl}/bookmark`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(bookmarkNotebookActionCreator(notebookName)));
  };
}

export function unbookmark(notebookName: string): any {
  const notebookUrl = getNotebookApiUrlFromName(notebookName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${notebookUrl}/unbookmark`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(unbookmarkNotebookActionCreator(notebookName)));
  };
}
