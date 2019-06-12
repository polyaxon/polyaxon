import { Action } from 'redux';
import * as url from 'url';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { BookmarkModel } from '../../models/bookmark';
import { NotebookModel } from '../../models/notebook';
import { urlifyProjectName } from '../../urls/utils';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';
import { stdFetchHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface FetchNotebooksRequestAction extends Action {
  type: actionTypes.FETCH_NOTEBOOKS_REQUEST;
}

export interface FetchNotebooksSuccessAction extends Action {
  type: actionTypes.FETCH_NOTEBOOKS_SUCCESS;
  notebooks: NotebookModel[];
  count: number;
}

export interface FetchNotebooksErrorAction extends Action {
  type: actionTypes.FETCH_NOTEBOOKS_ERROR;
  statusCode: number;
  error: any;
}

export function requestNotebooksActionCreator(): FetchNotebooksRequestAction {
  return {
    type: actionTypes.FETCH_NOTEBOOKS_REQUEST,
  };
}

export function receiveNotebooksActionCreator(notebooks: NotebookModel[],
                                              count: number): FetchNotebooksSuccessAction {
  return {
    type: actionTypes.FETCH_NOTEBOOKS_SUCCESS,
    notebooks,
    count
  };
}

export function fetchNotebooksErrorActionCreator(statusCode: number, error: any): FetchNotebooksErrorAction {
  return {
    type: actionTypes.FETCH_NOTEBOOKS_ERROR,
    statusCode,
    error,
  };
}

export function fetchBookmarkedNotebooksSuccessActionCreator(bookmarkedNotebooks: BookmarkModel[],
                                                             count: number): FetchNotebooksSuccessAction {
  const notebooks: NotebookModel[] = [];
  for (const bookmarkedNotebook of bookmarkedNotebooks) {
    notebooks.push(bookmarkedNotebook.content_object as NotebookModel);
  }
  return {
    type: actionTypes.FETCH_NOTEBOOKS_SUCCESS,
    notebooks,
    count
  };
}

export type FetchNotebookAction =
  FetchNotebooksRequestAction
  | FetchNotebooksSuccessAction
  | FetchNotebooksErrorAction;

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
      dispatch(fetchBookmarkedNotebooksSuccessActionCreator(results, count));
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
    .then((response) => stdFetchHandleError(
      response,
      dispatch,
      fetchNotebooksErrorActionCreator,
      'Notebooks not found',
      'Failed to fetch notebooks'))
    .then((response) => response.json())
    .then((json) => dispatchActionCreator(json.results, json.count))
    .catch((response) => {
      if (response.status === 400) {
        return response.value.json().then(
          (value: any) => dispatch(fetchNotebooksErrorActionCreator(response.status, value)));
      } else {
        return response.value;
      }
    });
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
