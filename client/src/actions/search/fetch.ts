import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { SearchModel } from '../../models/search';
import { getProjectUrlFromName } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface FetchSearchesRequestAction extends Action {
  type: actionTypes.FETCH_SEARCHES_REQUEST;
}

export interface FetchSearchesSuccessAction extends Action {
  type: actionTypes.FETCH_SEARCHES_SUCCESS;
  searches: SearchModel[];
  count: number;
}

export interface FetchSearchesErrorAction extends Action {
  type: actionTypes.FETCH_SEARCHES_ERROR;
  statusCode: number;
  error: any;
}

export function fetchSearchesRequestActionCreator(): FetchSearchesRequestAction {
  return {
    type: actionTypes.FETCH_SEARCHES_REQUEST,
  };
}

export function fetchSearchesSuccessActionCreator(searches: SearchModel[],
                                                  count: number): FetchSearchesSuccessAction {
  return {
    type: actionTypes.FETCH_SEARCHES_SUCCESS,
    searches,
    count
  };
}

export function fetchSearchesErrorActionCreator(statusCode: number, error: any): FetchSearchesErrorAction {
  return {
    type: actionTypes.FETCH_SEARCHES_ERROR,
    statusCode,
    error,
  };
}

export type FetchSearchAction =
  FetchSearchesRequestAction
  | FetchSearchesSuccessAction
  | FetchSearchesErrorAction;

function _fetchSearches(searchesUrl: string,
                        dispatch: any,
                        getState: any): any {
  dispatch(fetchSearchesRequestActionCreator());
  return fetch(
    searchesUrl, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
    .then((response) => stdHandleError(
      response,
      dispatch,
      fetchSearchesErrorActionCreator,
      'Searches not found',
      'Failed to fetch searches'))
    .then((response) => response.json())
    .then((json) => dispatch(fetchSearchesSuccessActionCreator(json.results, json.count)));
}

export function fetchExperimentGroupSearches(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches${getProjectUrlFromName(projectName, false)}/groups`;
    return _fetchSearches(searchesUrl, dispatch, getState);
  };
}

export function fetchExperimentSearches(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches${getProjectUrlFromName(projectName, false)}/experiments`;
    return _fetchSearches(searchesUrl, dispatch, getState);
  };
}

export function fetchJobSearches(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches${getProjectUrlFromName(projectName, false)}/jobs`;
    return _fetchSearches(searchesUrl, dispatch, getState);
  };
}

export function fetchBuildSearches(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches${getProjectUrlFromName(projectName, false)}/builds`;
    return _fetchSearches(searchesUrl, dispatch, getState);
  };
}

export function fetchNotebookSearches(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches${getProjectUrlFromName(projectName, false)}/notebooks`;
    return _fetchSearches(searchesUrl, dispatch, getState);
  };
}

export function fetchTensorboardSearches(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches${getProjectUrlFromName(projectName, false)}/tensorboards`;
    return _fetchSearches(searchesUrl, dispatch, getState);
  };
}
