import { Action } from 'redux';

import * as url from 'url';
import { BASE_API_URL } from '../../constants/api';
import { urlifyProjectName } from '../../constants/utils';
import history from '../../history';
import { BookmarkModel } from '../../models/bookmark';
import { BuildModel } from '../../models/build';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface FetchBuildsRequestAction extends Action {
  type: actionTypes.FETCH_BUILDS_REQUEST;
}

export interface FetchBuildsSuccessAction extends Action {
  type: actionTypes.FETCH_BUILDS_SUCCESS;
  builds: BuildModel[];
  count: number;
}

export interface FetchBuildsErrorAction extends Action {
  type: actionTypes.FETCH_BUILDS_ERROR;
  statusCode: number;
  error: any;
}

export function fetchBuildsRequestActionCreator(): FetchBuildsRequestAction {
  return {
    type: actionTypes.FETCH_BUILDS_REQUEST,
  };
}

export function fetchBookmarkedBuildsSuccessActionCreator(bookmarkedBuilds: BookmarkModel[],
                                                          count: number): FetchBuildsSuccessAction {
  const builds: BuildModel[] = [];
  for (const bookmarkedBuild of bookmarkedBuilds) {
    builds.push(bookmarkedBuild.content_object as BuildModel);
  }
  return {
    type: actionTypes.FETCH_BUILDS_SUCCESS,
    builds,
    count
  };
}

export function fetchBuildsSuccessActionCreator(builds: BuildModel[], count: number): FetchBuildsSuccessAction {
  return {
    type: actionTypes.FETCH_BUILDS_SUCCESS,
    builds,
    count
  };
}

export function fetchBuildsErrorActionCreator(statusCode: number, error: any): FetchBuildsErrorAction {
  return {
    type: actionTypes.FETCH_BUILDS_ERROR,
    statusCode,
    error,
  };
}

export type FetchBuildAction =
  | FetchBuildsRequestAction
  | FetchBuildsSuccessAction
  | FetchBuildsErrorAction;

function _fetchBuilds(buildsUrl: string,
                      endpointList: string,
                      filters: { [key: string]: number | boolean | string } = {},
                      dispatch: any,
                      getState: any): any {
  dispatch(fetchBuildsRequestActionCreator());

  const urlPieces = location.hash.split('?');
  const baseUrl = urlPieces[0];
  if (Object.keys(filters).length) {
    buildsUrl += url.format({query: filters});
    if (baseUrl) {
      history.push(baseUrl + url.format({query: filters}));
    }
  } else if (urlPieces.length > 1) {
    history.push(baseUrl);
  }

  const dispatchActionCreator = (results: any, count: number) => {
    if (endpointList === BOOKMARKS) {
      dispatch(fetchBookmarkedBuildsSuccessActionCreator(results, count));
    } else {
      dispatch(fetchBuildsSuccessActionCreator(results, count));
    }
  };

  return fetch(
    buildsUrl, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
    .then((response) => stdHandleError(
        response,
        dispatch,
        fetchBuildsErrorActionCreator,
        'Builds not found',
        'Failed to fetch builds'))
    .then((response) => response.json())
    .then((json) => dispatchActionCreator(json.results, json.count));
}

export function fetchBookmarkedBuilds(user: string,
                                      filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const buildsUrl = `${BASE_API_URL}/bookmarks/${user}/builds/`;
    return _fetchBuilds(buildsUrl, BOOKMARKS, filters, dispatch, getState);
  };
}

export function fetchArchivedBuilds(user: string,
                                    filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const buildsUrl = `${BASE_API_URL}/archives/${user}/builds/`;
    return _fetchBuilds(buildsUrl, ARCHIVES, filters, dispatch, getState);
  };
}

export function fetchBuilds(projectUniqueName: string,
                            filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const buildsUrl = `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/builds`;
    return _fetchBuilds(buildsUrl, '', filters, dispatch, getState);
  };
}
