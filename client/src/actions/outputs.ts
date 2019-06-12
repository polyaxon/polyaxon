import { Action } from 'redux';

import { BASE_API_URL } from '../constants/api';
import { urlifyProjectName } from '../urls/utils';
import { stdHandleError } from './utils';

export enum actionTypes {
  FETCH_OUTPUTS_TREE_REQUEST = 'FETCH_OUTPUTS_TREE_REQUEST',
  FETCH_OUTPUTS_TREE_SUCCESS = 'FETCH_OUTPUTS_TREE_SUCCESS',
  FETCH_OUTPUTS_TREE_ERROR = 'FETCH_OUTPUTS_TREE_ERROR',
  FETCH_OUTPUTS_FILE_REQUEST = 'FETCH_OUTPUTS_FILE_REQUEST',
  FETCH_OUTPUTS_FILE_SUCCESS = 'FETCH_OUTPUTS_FILE_SUCCESS',
  FETCH_OUTPUTS_FILE_ERROR = 'FETCH_OUTPUTS_FILE_ERROR',
}

export interface FetchOutputsTreeRequestAction extends Action {
  type: actionTypes.FETCH_OUTPUTS_TREE_REQUEST;
  path: string;
}

export interface FetchOutputsTreeSuccessAction extends Action {
  type: actionTypes.FETCH_OUTPUTS_TREE_SUCCESS;
  path: string;
  outputsTree: { [key: string]: any };
}

export interface FetchOutputsTreeErrorAction extends Action {
  type: actionTypes.FETCH_OUTPUTS_TREE_ERROR;
  statusCode: number;
  error: any;
  path: string;
}

export interface FetchOutputsFileRequestAction extends Action {
  type: actionTypes.FETCH_OUTPUTS_FILE_REQUEST;
  path: string;
  outputsFile: string;
}

export interface FetchOutputsFileSuccessAction extends Action {
  type: actionTypes.FETCH_OUTPUTS_FILE_SUCCESS;
  path: string;
  outputsFile: string;
}

export interface FetchOutputsFileErrorAction extends Action {
  type: actionTypes.FETCH_OUTPUTS_FILE_ERROR;
  statusCode: number;
  error: any;
  path: string;
}

export function fetchOutputsTreeRequestActionCreator(path: string): FetchOutputsTreeRequestAction {
  return {
    type: actionTypes.FETCH_OUTPUTS_TREE_REQUEST,
    path
  };
}

export function fetchOutputsTreeSuccessActionCreator(
  path: string,
  outputsTree: { [key: string]: any }): FetchOutputsTreeSuccessAction {
  return {
    type: actionTypes.FETCH_OUTPUTS_TREE_SUCCESS,
    path,
    outputsTree
  };
}

export function fetchOutputsTreeErrorActionCreator(statusCode: number,
                                                   error: any,
                                                   path: string): FetchOutputsTreeErrorAction {
  return {
    type: actionTypes.FETCH_OUTPUTS_TREE_ERROR,
    statusCode,
    error,
    path
  };
}

export function fetchOutputsFileRequestActionCreator(path: string): FetchOutputsFileRequestAction {
  return {
    type: actionTypes.FETCH_OUTPUTS_FILE_REQUEST,
    path,
    outputsFile: ''
  };
}

export function fetchOutputsFileSuccessActionCreator(path: string,
                                                     outputsFile: string): FetchOutputsFileSuccessAction {
  return {
    type: actionTypes.FETCH_OUTPUTS_FILE_SUCCESS,
    path,
    outputsFile
  };
}

export function fetchOutputsFileErrorActionCreator(statusCode: number,
                                                   error: any,
                                                   path: string): FetchOutputsFileErrorAction {
  return {
    type: actionTypes.FETCH_OUTPUTS_FILE_ERROR,
    statusCode,
    error,
    path
  };
}

export type OutputsAction =
  FetchOutputsTreeRequestAction
  | FetchOutputsTreeSuccessAction
  | FetchOutputsTreeErrorAction
  | FetchOutputsFileRequestAction
  | FetchOutputsFileSuccessAction
  | FetchOutputsFileErrorAction;

export function fetchOutputsTree(projectUniqueName: string,
                                 resources: string,
                                 id: number,
                                 path: string): any {
  return (dispatch: any, getState: any) => {
    dispatch(fetchOutputsTreeRequestActionCreator(path));

    let logsUrl =
      `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/outputs/tree`;

    if (path) {
      logsUrl += `?path=${path}`;
    }

    return fetch(logsUrl, {
      headers: {
        'Content-Type': 'text/plain;charset=UTF-8',
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        fetchOutputsTreeErrorActionCreator,
        'Logs not outputs',
        'Failed to fetch outputs',
        [path]))
      .then((response) => response.json())
      .then((json) => dispatch(fetchOutputsTreeSuccessActionCreator(path, json)));
  };
}

export function fetchOutputsFile(projectUniqueName: string,
                                 resources: string,
                                 id: number,
                                 path: string,
                                 filetype: string): any {
  return (dispatch: any, getState: any) => {
    dispatch(fetchOutputsFileRequestActionCreator(path));

    const logsUrl =
      `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/outputs/files?path=${path}`;

    return fetch(logsUrl, {
      headers: {
        'Content-Type': 'text/plain;charset=UTF-8',
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        fetchOutputsFileErrorActionCreator,
        'File not found',
        'Failed to fetch file',
        [path]))
      .then((response) => {
        if (filetype === 'img') {
          return response.blob();
        }
        return response.text();
      })
      .then((val) => {
        if (filetype === 'img') {
          return dispatch(fetchOutputsFileSuccessActionCreator(path, URL.createObjectURL(val)));
        }
        return dispatch(fetchOutputsFileSuccessActionCreator(path, val));
      });
  };
}
