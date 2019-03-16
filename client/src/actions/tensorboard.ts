import { Action } from 'redux';
import * as url from 'url';

import { BASE_API_URL } from '../constants/api';
import {
  getProjectUrl,
  getTensorboardApiUrl,
  getTensorboardApiUrlFromName,
  handleAuthError,
  urlifyProjectName
} from '../constants/utils';
import history from '../history';
import { BookmarkModel } from '../models/bookmark';
import { TensorboardModel } from '../models/tensorboard';
import { ARCHIVES, BOOKMARKS } from '../utils/endpointList';

export enum actionTypes {
  CREATE_TENSORBOARD = 'CREATE_TENSORBOARD',
  DELETE_TENSORBOARD = 'DELETE_TENSORBOARD',
  STOP_TENSORBOARD = 'STOP_TENSORBOARD',
  ARCHIVE_TENSORBOARD = 'ARCHIVE_TENSORBOARD',
  RESTORE_TENSORBOARD = 'RESTORE_TENSORBOARD',
  UPDATE_TENSORBOARD = 'UPDATE_TENSORBOARD',
  RECEIVE_TENSORBOARD = 'RECEIVE_TENSORBOARD',
  RECEIVE_TENSORBOARDS = 'RECEIVE_TENSORBOARDS',
  REQUEST_TENSORBOARD = 'REQUEST_TENSORBOARD',
  REQUEST_TENSORBOARDS = 'REQUEST_TENSORBOARDS',
  BOOKMARK_TENSORBOARD = 'BOOKMARK_TENSORBOARD',
  UNBOOKMARK_TENSORBOARD = 'UNBOOKMARK_TENSORBOARD',
}

export interface CreateUpdateReceiveTensorboardAction extends Action {
  type: actionTypes.CREATE_TENSORBOARD | actionTypes.UPDATE_TENSORBOARD | actionTypes.RECEIVE_TENSORBOARD;
  tensorboard: TensorboardModel;
}

export interface DeleteTensorboardAction extends Action {
  type: actionTypes.DELETE_TENSORBOARD;
  tensorboardName: string;
}

export interface ArchiveTensorboardAction extends Action {
  type: actionTypes.ARCHIVE_TENSORBOARD;
  tensorboardName: string;
}

export interface RestoreTensorboardAction extends Action {
  type: actionTypes.RESTORE_TENSORBOARD;
  tensorboardName: string;
}

export interface StopTensorboardAction extends Action {
  type: actionTypes.STOP_TENSORBOARD;
  tensorboardName: string;
}

export interface BookmarkTensorboardAction extends Action {
  type: actionTypes.BOOKMARK_TENSORBOARD | actionTypes.UNBOOKMARK_TENSORBOARD;
  tensorboardName: string;
}

export interface ReceiveTensorboardsAction extends Action {
  type: actionTypes.RECEIVE_TENSORBOARDS;
  tensorboards: TensorboardModel[];
  count: number;
}

export interface RequestTensorboardsAction extends Action {
  type: actionTypes.REQUEST_TENSORBOARDS | actionTypes.REQUEST_TENSORBOARD;
}

export type TensorboardAction =
  CreateUpdateReceiveTensorboardAction
  | DeleteTensorboardAction
  | StopTensorboardAction
  | ArchiveTensorboardAction
  | RestoreTensorboardAction
  | ReceiveTensorboardsAction
  | RequestTensorboardsAction
  | BookmarkTensorboardAction;

export function createTensorboardActionCreator(tensorboard: TensorboardModel): CreateUpdateReceiveTensorboardAction {
  return {
    type: actionTypes.CREATE_TENSORBOARD,
    tensorboard
  };
}

export function updateTensorboardActionCreator(tensorboard: TensorboardModel): CreateUpdateReceiveTensorboardAction {
  return {
    type: actionTypes.UPDATE_TENSORBOARD,
    tensorboard
  };
}

export function deleteTensorboardActionCreator(tensorboardName: string): DeleteTensorboardAction {
  return {
    type: actionTypes.DELETE_TENSORBOARD,
    tensorboardName
  };
}

export function stopTensorboardActionCreator(tensorboardName: string): StopTensorboardAction {
  return {
    type: actionTypes.STOP_TENSORBOARD,
    tensorboardName
  };
}

export function archiveTensorboardActionCreator(tensorboardName: string): ArchiveTensorboardAction {
  return {
    type: actionTypes.ARCHIVE_TENSORBOARD,
    tensorboardName
  };
}

export function restoreTensorboardActionCreator(tensorboardName: string): RestoreTensorboardAction {
  return {
    type: actionTypes.RESTORE_TENSORBOARD,
    tensorboardName
  };
}

export function requestTensorboardActionCreator(): RequestTensorboardsAction {
  return {
    type: actionTypes.REQUEST_TENSORBOARD,
  };
}

export function requestTensorboardsActionCreator(): RequestTensorboardsAction {
  return {
    type: actionTypes.REQUEST_TENSORBOARDS,
  };
}

export function receiveTensorboardActionCreator(tensorboard: TensorboardModel): CreateUpdateReceiveTensorboardAction {
  return {
    type: actionTypes.RECEIVE_TENSORBOARD,
    tensorboard
  };
}

export function receiveTensorboardsActionCreator(tensorboards: TensorboardModel[],
                                                 count: number): ReceiveTensorboardsAction {
  return {
    type: actionTypes.RECEIVE_TENSORBOARDS,
    tensorboards,
    count
  };
}

export function receiveBookmarkedTensorboardsActionCreator(bookmarkedTensorboards: BookmarkModel[],
                                                           count: number): ReceiveTensorboardsAction {
  const tensorboards: TensorboardModel[] = [];
  for (const bookmarkedTensorboard of bookmarkedTensorboards) {
    tensorboards.push(bookmarkedTensorboard.content_object as TensorboardModel);
  }
  return {
    type: actionTypes.RECEIVE_TENSORBOARDS,
    tensorboards,
    count
  };
}

export function bookmarkTensorboardActionCreator(tensorboardName: string) {
  return {
    type: actionTypes.BOOKMARK_TENSORBOARD,
    tensorboardName,
  };
}

export function unbookmarkTensorboardActionCreator(tensorboardName: string) {
  return {
    type: actionTypes.UNBOOKMARK_TENSORBOARD,
    tensorboardName,
  };
}

function _fetchTensorboards(tensorboardsUrl: string,
                            endpointList: string,
                            filters: { [key: string]: number | boolean | string } = {},
                            dispatch: any,
                            getState: any): any {
  dispatch(requestTensorboardsActionCreator());
  const urlPieces = location.hash.split('?');
  const baseUrl = urlPieces[0];
  if (Object.keys(filters).length) {
    tensorboardsUrl += url.format({query: filters});
    if (baseUrl) {
      history.push(baseUrl + url.format({query: filters}));
    }
  } else if (urlPieces.length > 1) {
    history.push(baseUrl);
  }

  const dispatchActionCreator = (results: any, count: number) => {
    if (endpointList === BOOKMARKS) {
      dispatch(receiveBookmarkedTensorboardsActionCreator(results, count));
    } else {
      dispatch(receiveTensorboardsActionCreator(results, count));
    }
  };

  return fetch(
    tensorboardsUrl, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
    .then((response) => handleAuthError(response, dispatch))
    .then((response) => response.json())
    .then((json) => dispatchActionCreator(json.results, json.count));
}

export function fetchBookmarkedTensorboards(user: string,
                                            filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const tensorboardsUrl = `${BASE_API_URL}/bookmarks/${user}/tensorboards/`;
    return _fetchTensorboards(tensorboardsUrl, BOOKMARKS, filters, dispatch, getState);
  };
}

export function fetchArchivedTensorboards(user: string,
                                          filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const tensorboardsUrl = `${BASE_API_URL}/archives/${user}/tensorboards/`;
    return _fetchTensorboards(tensorboardsUrl, ARCHIVES, filters, dispatch, getState);
  };
}

export function fetchTensorboards(projectUniqueName: string,
                                  filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const tensorboardsUrl = `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/tensorboards`;
    return _fetchTensorboards(tensorboardsUrl, '', filters, dispatch, getState);
  };
}

export function fetchTensorboard(user: string, projectName: string, tensorboardId: number | string): any {
  const tensorboardUrl = getTensorboardApiUrl(user, projectName, tensorboardId, false);
  return (dispatch: any, getState: any) => {
    dispatch(requestTensorboardActionCreator());
    return fetch(
      `${BASE_API_URL}${tensorboardUrl}`, {
        headers: {
          Authorization: 'token ' + getState().auth.token
        }
      })
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.json())
      .then((json) => dispatch(receiveTensorboardActionCreator(json)));
  };
}

export function updateTensorboard(tensorboardName: string, updateDict: { [key: string]: any }): any {
  const tensorboardUrl = getTensorboardApiUrlFromName(tensorboardName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${tensorboardUrl}`, {
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
      .then((json) => dispatch(updateTensorboardActionCreator(json)));
  };
}

export function deleteTensorboard(tensorboardName: string, redirect: boolean = false): any {
  const tensorboardUrl = getTensorboardApiUrlFromName(tensorboardName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${tensorboardUrl}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => {
        const dispatched = dispatch(deleteTensorboardActionCreator(tensorboardName));
        if (redirect) {
          const values = tensorboardName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#tensorboards');
        }
        return dispatched;
      });
  };
}

export function archiveTensorboard(tensorboardName: string, redirect: boolean = false): any {
  const tensorboardUrl = getTensorboardApiUrlFromName(tensorboardName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${tensorboardUrl}/archive`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => {
        const dispatched = dispatch(archiveTensorboardActionCreator(tensorboardName));
        if (redirect) {
          const values = tensorboardName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#tensorboards');
        }
        return dispatched;
      });
  };
}

export function restoreTensorboard(tensorboardName: string): any {
  const tensorboardUrl = getTensorboardApiUrlFromName(tensorboardName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${tensorboardUrl}/restore`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(restoreTensorboardActionCreator(tensorboardName)));
  };
}

export function stopTensorboard(tensorboardName: string): any {
  const tensorboardUrl = getTensorboardApiUrlFromName(tensorboardName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${tensorboardUrl}/stop`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(stopTensorboardActionCreator(tensorboardName)));
  };
}

export function bookmark(tensorboardName: string): any {
  const tensorboardUrl = getTensorboardApiUrlFromName(tensorboardName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${tensorboardUrl}/bookmark`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(bookmarkTensorboardActionCreator(tensorboardName)));
  };
}

export function unbookmark(tensorboardName: string): any {
  const tensorboardUrl = getTensorboardApiUrlFromName(tensorboardName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${tensorboardUrl}/unbookmark`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(unbookmarkTensorboardActionCreator(tensorboardName)));
  };
}
