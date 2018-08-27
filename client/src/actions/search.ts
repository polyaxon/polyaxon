import { Action } from 'redux';

import { BASE_API_URL } from '../constants/api';
import {
  getProjectUrlFromName,
  handleAuthError
} from '../constants/utils';
import { SearchModel } from '../models/search';

export enum actionTypes {
  RECEIVE_SEARCH = 'RECEIVE_SEARCH',
  DELETE_SEARCH = 'DELETE_SEARCH',
  RECEIVE_SEARCHES = 'RECEIVE_SEARCHES',
  REQUEST_SEARCHES = 'REQUEST_SEARCHES',
}

export interface ReceiveSearchAction extends Action {
  type: actionTypes.RECEIVE_SEARCH;
  search: SearchModel;
}

export interface DeleteSearchAction extends Action {
  type: actionTypes.DELETE_SEARCH;
  searchId: number;
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
  | ReceiveSearchAction
  | DeleteSearchAction
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

export function receiveSearchActionCreator(search: SearchModel): ReceiveSearchAction {
  return {
    type: actionTypes.RECEIVE_SEARCH,
    search,
  };
}

export function deleteSearchActionCreator(searchId: number): DeleteSearchAction {
  return {
    type: actionTypes.DELETE_SEARCH,
    searchId,
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

function _createSearch(searchesUrl: string,
                       data: SearchModel,
                       dispatch: any,
                       getState: any): any {
  delete data.id;
  if (!data.name) {
    delete data.name;
  }
  return fetch(
    searchesUrl, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
    .then((response) => handleAuthError(response, dispatch))
    .then((response) => response.json())
    .then((json) => dispatch(receiveSearchActionCreator(json)));
}

function _deleteSearches(searchesUrl: string,
                         searchId: number,
                         dispatch: any,
                         getState: any): any {
  return fetch(
    searchesUrl, {
      method: 'DELETE',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      },
    })
    .then((response) => handleAuthError(response, dispatch))
    .then((json) => dispatch(deleteSearchActionCreator(searchId)));
}

export function fetchExperimentGroupSearches(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches/${getProjectUrlFromName(projectName, false)}/groups`;
    return _fetchSearches(searchesUrl, dispatch, getState);
  };
}

export function createExperimentGroupSearch(projectName: string, data: SearchModel): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches/${getProjectUrlFromName(projectName, false)}/groups`;
    return _createSearch(searchesUrl, data, dispatch, getState);
  };
}

export function deleteExperimentGroupSearch(projectName: string, searchId: number): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches/${getProjectUrlFromName(projectName, false)}/groups/${searchId}`;
    return _deleteSearches(searchesUrl, searchId, dispatch, getState);
  };
}

export function fetchExperimentSearches(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches/${getProjectUrlFromName(projectName, false)}/experiments`;
    return _fetchSearches(searchesUrl, dispatch, getState);
  };
}

export function createExperimentSearch(projectName: string, data: SearchModel): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches/${getProjectUrlFromName(projectName, false)}/experiments`;
    return _createSearch(searchesUrl, data, dispatch, getState);
  };
}

export function deleteExperimentSearch(projectName: string, searchId: number): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches/${getProjectUrlFromName(projectName, false)}/experiments/${searchId}`;
    return _deleteSearches(searchesUrl, searchId, dispatch, getState);
  };
}

export function fetchJobSearches(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches/${getProjectUrlFromName(projectName, false)}/jobs`;
    return _fetchSearches(searchesUrl, dispatch, getState);
  };
}

export function createJobSearch(projectName: string, data: SearchModel): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches/${getProjectUrlFromName(projectName, false)}/jobs`;
    return _createSearch(searchesUrl, data, dispatch, getState);
  };
}

export function deleteJobSearch(projectName: string, searchId: number): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches/${getProjectUrlFromName(projectName, false)}/jobs/${searchId}`;
    return _deleteSearches(searchesUrl, searchId, dispatch, getState);
  };
}

export function fetchBuildSearches(projectName: string): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches/${getProjectUrlFromName(projectName, false)}/builds`;
    return _fetchSearches(searchesUrl, dispatch, getState);
  };
}

export function createBuildSearch(projectName: string, data: SearchModel): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches/${getProjectUrlFromName(projectName, false)}/builds`;
    return _createSearch(searchesUrl, data, dispatch, getState);
  };
}

export function deleteBuildSearch(projectName: string, searchId: number): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches/${getProjectUrlFromName(projectName, false)}/builds/${searchId}`;
    return _deleteSearches(searchesUrl, searchId, dispatch, getState);
  };
}
