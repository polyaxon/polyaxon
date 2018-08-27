import { Action } from 'redux';

import { BASE_API_URL } from '../constants/api';
import {
  getProjectUrlFromName,
  handleAuthError
} from '../constants/utils';
import { SearchModel } from '../models/search';

export enum actionTypes {
  RECEIVE_SEARCHES = 'RECEIVE_SEARCHES',
  REQUEST_SEARCHES = 'REQUEST_SEARCHES',
}

export interface ReceiveSearchesAction extends Action {
  type: actionTypes.RECEIVE_SEARCHES;
  searches: SearchModel[];
  count: number;
}

export interface RequestSearchesAction extends Action {
  type: actionTypes.REQUEST_SEARCHES;
}

export type SearchAction =
  | ReceiveSearchesAction
  | RequestSearchesAction;

export function requestSearchesActionCreator(): RequestSearchesAction {
  return {
    type: actionTypes.REQUEST_SEARCHES,
  };
}

export function receiveSearchesActionCreator(searches: SearchModel[],
                                             count: number): ReceiveSearchesAction {
  return {
    type: actionTypes.RECEIVE_SEARCHES,
    searches,
    count
  };
}

function _fetchSearches(searchesUrl: string,
                        dispatch: any,
                        getState: any): any {
  dispatch(requestSearchesActionCreator());
  return fetch(
    searchesUrl, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
    .then((response) => handleAuthError(response, dispatch))
    .then((response) => response.json())
    .then((json) => dispatch(receiveSearchesActionCreator(json.results, json.count)));
}

export function fetchProjectExperimentGroupSearches(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches/${getProjectUrlFromName(projectName, false)}/groups`;
    return _fetchSearches(searchesUrl, dispatch, getState);
  };
}

export function fetchProjectExperimentSearches(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches/${getProjectUrlFromName(projectName, false)}/experiments`;
    return _fetchSearches(searchesUrl, dispatch, getState);
  };
}

export function fetchProjectJobSearches(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches/${getProjectUrlFromName(projectName, false)}/jobs`;
    return _fetchSearches(searchesUrl, dispatch, getState);
  };
}

export function fetchProjectBuildSearches(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches/${getProjectUrlFromName(projectName, false)}/builds`;
    return _fetchSearches(searchesUrl, dispatch, getState);
  };
}
