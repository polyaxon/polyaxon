import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getProjectUrlFromName } from '../../constants/utils';
import { SearchModel } from '../../models/search';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';
import { getSearchSuccessActionCreator } from './get';

export interface CreateUpdateRequestSearchAction extends Action {
  type: actionTypes.CREATE_SEARCH_REQUEST;
}

export interface CreateUpdateSuccessSearchAction extends Action {
  type: actionTypes.CREATE_SEARCH_SUCCESS;
}

export interface CreateUpdateErrorSearchAction extends Action {
  type: actionTypes.CREATE_SEARCH_ERROR;
  statusCode: number;
  error: any;
}

export function createSearchRequestActionCreator(): CreateUpdateRequestSearchAction {
  return {
    type: actionTypes.CREATE_SEARCH_REQUEST,
  };
}

export function createSearchSuccessActionCreator(): CreateUpdateSuccessSearchAction {
  return {
    type: actionTypes.CREATE_SEARCH_SUCCESS,
  };
}

export function createSearchErrorActionCreator(statusCode: number, error: any): CreateUpdateErrorSearchAction {
  return {
    type: actionTypes.CREATE_SEARCH_ERROR,
    statusCode,
    error,
  };
}

export type CreateSearchAction =
  | CreateUpdateRequestSearchAction
  | CreateUpdateSuccessSearchAction
  | CreateUpdateErrorSearchAction;

function _createSearch(searchesUrl: string,
                       data: SearchModel,
                       dispatch: any,
                       getState: any): any {
  delete data.id;
  if (!data.name) {
    delete data.name;
  }

  dispatch(createSearchRequestActionCreator());

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
    .then((response) => stdCreateHandleError(
      response,
      dispatch,
      createSearchErrorActionCreator,
      'Not found',
      'Failed to create search'))
    .then((response) => response.json())
    .then((json) => {
      dispatch(createSearchSuccessActionCreator());
      return dispatch(getSearchSuccessActionCreator(json));
    })
    .catch((response) => {
      if (response.status === 400) {
        return response.value.json().then(
          (value: any) => dispatch(createSearchErrorActionCreator(response.status, value)));
      } else {
        return response.value;
      }
    });
}


export function createExperimentGroupSearch(projectName: string, data: SearchModel): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches${getProjectUrlFromName(projectName, false)}/groups`;
    return _createSearch(searchesUrl, data, dispatch, getState);
  };
}


export function createExperimentSearch(projectName: string, data: SearchModel): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches${getProjectUrlFromName(projectName, false)}/experiments`;
    return _createSearch(searchesUrl, data, dispatch, getState);
  };
}


export function createJobSearch(projectName: string, data: SearchModel): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches${getProjectUrlFromName(projectName, false)}/jobs`;
    return _createSearch(searchesUrl, data, dispatch, getState);
  };
}


export function createBuildSearch(projectName: string, data: SearchModel): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches${getProjectUrlFromName(projectName, false)}/builds`;
    return _createSearch(searchesUrl, data, dispatch, getState);
  };
}


export function createNotebookSearch(projectName: string, data: SearchModel): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches${getProjectUrlFromName(projectName, false)}/notebooks`;
    return _createSearch(searchesUrl, data, dispatch, getState);
  };
}


export function createTensorboardSearch(projectName: string, data: SearchModel): any {
  return (dispatch: any, getState: any) => {
    const searchesUrl = `${BASE_API_URL}/searches${getProjectUrlFromName(projectName, false)}/tensorboards`;
    return _createSearch(searchesUrl, data, dispatch, getState);
  };
}
