import { Action } from 'redux';
import * as url from 'url';

import { BASE_API_URL } from '../../constants/api';
import { urlifyProjectName } from '../../constants/utils';
import history from '../../history';
import { BookmarkModel } from '../../models/bookmark';
import { TensorboardModel } from '../../models/tensorboard';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface FetchTensorboardsRequestAction extends Action {
  type: actionTypes.FETCH_TENSORBOARDS_REQUEST;
}

export interface FetchTensorboardsSuccessAction extends Action {
  type: actionTypes.FETCH_TENSORBOARDS_SUCCESS;
  tensorboards: TensorboardModel[];
  count: number;
}

export interface FetchTensorboardsErrorAction extends Action {
  type: actionTypes.FETCH_TENSORBOARDS_ERROR;
  statusCode: number;
  error: any;
}

export function fetchTensorboardsRequestActionCreator(): FetchTensorboardsRequestAction {
  return {
    type: actionTypes.FETCH_TENSORBOARDS_REQUEST,
  };
}

export function FetchTensorboardsSuccessActionCreator(tensorboards: TensorboardModel[],
                                                      count: number): FetchTensorboardsSuccessAction {
  return {
    type: actionTypes.FETCH_TENSORBOARDS_SUCCESS,
    tensorboards,
    count
  };
}

export function fetchTensorboardsErrorActionCreator(statusCode: number, error: any): FetchTensorboardsErrorAction {
  return {
    type: actionTypes.FETCH_TENSORBOARDS_ERROR,
    statusCode,
    error,
  };
}

export function fetchBookmarkedTensorboardsSuccessActionCreator(bookmarkedTensorboards: BookmarkModel[],
                                                                count: number): FetchTensorboardsSuccessAction {
  const tensorboards: TensorboardModel[] = [];
  for (const bookmarkedTensorboard of bookmarkedTensorboards) {
    tensorboards.push(bookmarkedTensorboard.content_object as TensorboardModel);
  }
  return {
    type: actionTypes.FETCH_TENSORBOARDS_SUCCESS,
    tensorboards,
    count
  };
}

export type FetchTensorboardAction =
  FetchTensorboardsRequestAction
  | FetchTensorboardsSuccessAction
  | FetchTensorboardsErrorAction;

function _fetchTensorboards(tensorboardsUrl: string,
                            endpointList: string,
                            filters: { [key: string]: number | boolean | string } = {},
                            dispatch: any,
                            getState: any): any {

  dispatch(fetchTensorboardsRequestActionCreator());

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
      dispatch(fetchBookmarkedTensorboardsSuccessActionCreator(results, count));
    } else {
      dispatch(FetchTensorboardsSuccessActionCreator(results, count));
    }
  };

  return fetch(
    tensorboardsUrl, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
    .then((response) => stdHandleError(
      response,
      dispatch,
      fetchTensorboardsErrorActionCreator,
      'Tensorboards not found',
      'Failed to fetch tensorboards'))
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
