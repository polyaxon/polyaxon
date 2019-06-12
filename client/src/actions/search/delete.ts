import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getProjectUrlFromName } from '../../urls/utils';
import { stdDeleteHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface DeleteSearchRequestAction extends Action {
  type: actionTypes.DELETE_SEARCH_REQUEST;
  searchId: number;
}

export interface DeleteSearchSuccessAction extends Action {
  type: actionTypes.DELETE_SEARCH_SUCCESS;
  searchId: number;
}

export interface DeleteSearchErrorAction extends Action {
  type: actionTypes.DELETE_SEARCH_ERROR;
  statusCode: number;
  error: any;
  searchId: number;
}

export function deleteSearchRequestActionCreator(searchId: number): DeleteSearchRequestAction {
  return {
    type: actionTypes.DELETE_SEARCH_REQUEST,
    searchId,
  };
}

export function deleteSearchSuccessActionCreator(searchId: number): DeleteSearchSuccessAction {
  return {
    type: actionTypes.DELETE_SEARCH_SUCCESS,
    searchId,
  };
}

export function deleteSearchErrorActionCreator(statusCode: number,
                                               error: any,
                                               searchId: number): DeleteSearchErrorAction {
  return {
    type: actionTypes.DELETE_SEARCH_ERROR,
    statusCode,
    error,
    searchId,
  };
}

export type DeleteSearchAction =
  DeleteSearchRequestAction
  | DeleteSearchSuccessAction
  | DeleteSearchErrorAction;

function _deleteSearches(searchesUrl: string,
                         searchId: number,
                         dispatch: any,
                         getState: any): any {

  dispatch(deleteSearchRequestActionCreator(searchId));

  return fetch(
    searchesUrl, {
      method: 'DELETE',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      },
    })
    .then((response) => stdDeleteHandleError(
      response,
      dispatch,
      deleteSearchErrorActionCreator,
      'Search not found',
      'Failed to delete search',
      [searchId]))
    .then((json) => dispatch(deleteSearchSuccessActionCreator(searchId)));
}

export function deleteExperimentGroupSearch(projectName: string, searchId: number): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches${getProjectUrlFromName(projectName, false)}/groups/${searchId}`;
    return _deleteSearches(searchesUrl, searchId, dispatch, getState);
  };
}

export function deleteTensorboardSearch(projectName: string, searchId: number): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches${getProjectUrlFromName(
      projectName, false)}/tensorboards/${searchId}`;
    return _deleteSearches(searchesUrl, searchId, dispatch, getState);
  };
}

export function deleteNotebookSearch(projectName: string, searchId: number): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches${getProjectUrlFromName(projectName, false)}/notebooks/${searchId}`;
    return _deleteSearches(searchesUrl, searchId, dispatch, getState);
  };
}

export function deleteBuildSearch(projectName: string, searchId: number): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches${getProjectUrlFromName(projectName, false)}/builds/${searchId}`;
    return _deleteSearches(searchesUrl, searchId, dispatch, getState);
  };
}

export function deleteJobSearch(projectName: string, searchId: number): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches${getProjectUrlFromName(projectName, false)}/jobs/${searchId}`;
    return _deleteSearches(searchesUrl, searchId, dispatch, getState);
  };
}

export function deleteExperimentSearch(projectName: string, searchId: number): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches${getProjectUrlFromName(projectName, false)}/experiments/${searchId}`;
    return _deleteSearches(searchesUrl, searchId, dispatch, getState);
  };
}
