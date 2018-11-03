import { Action } from 'redux';
import { BASE_API_URL } from '../constants/api';
import { handleAuthError, urlifyProjectName } from '../constants/utils';

export enum actionTypes {
  RECEIVE_OUTPUTS_TREE = 'RECEIVE_OUTPUTS_TREE',
  REQUEST_OUTPUTS_TREE = 'REQUEST_OUTPUTS_TREE',
  RECEIVE_OUTPUTS_FILE = 'RECEIVE_OUTPUTS_FILE',
  REQUEST_OUTPUTS_FILE = 'REQUEST_OUTPUTS_FILE',
}

export interface RequestOutputsTreeAction extends Action {
  type: actionTypes.REQUEST_OUTPUTS_TREE;
  outputsTree: { [key: string]: any };
}

export interface ReceiveOutputsTreeAction extends Action {
  type: actionTypes.RECEIVE_OUTPUTS_TREE;
  path: string;
  outputsTree: { [key: string]: any };
}

export interface RequestOutputsFileAction extends Action {
  type: actionTypes.REQUEST_OUTPUTS_FILE;
  outputsFile: string;
}

export interface ReceiveOutputsFileAction extends Action {
  type: actionTypes.RECEIVE_OUTPUTS_FILE;
  outputsFile: string;
}

export function requestOutputsTreeActionCreator(): RequestOutputsTreeAction {
  return {
    type: actionTypes.REQUEST_OUTPUTS_TREE,
    outputsTree: {}
  };
}

export function receiveOutputsTreeActionCreator(path: string,
                                                outputsTree: { [key: string]: any }): ReceiveOutputsTreeAction {
  return {
    type: actionTypes.RECEIVE_OUTPUTS_TREE,
    path,
    outputsTree
  };
}

export function requestOutputsFileActionCreator(): RequestOutputsFileAction {
  return {
    type: actionTypes.REQUEST_OUTPUTS_FILE,
    outputsFile: ''
  };
}

export function receiveOutputsFileActionCreator(outputsFile: string): ReceiveOutputsFileAction {
  return {
    type: actionTypes.RECEIVE_OUTPUTS_FILE,
    outputsFile
  };
}

export type OutputsAction =
  RequestOutputsTreeAction
  | ReceiveOutputsTreeAction
  | ReceiveOutputsFileAction
  | ReceiveOutputsFileAction;

export function fetchOutputsTree(projectUniqueName: string,
                                 resources: string,
                                 id: number,
                                 path: string): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestOutputsTreeActionCreator());

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
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.json())
      .then((json) => dispatch(receiveOutputsTreeActionCreator(path, json)));
  };
}

export function fetchOutputsFile(projectUniqueName: string, resources: string, id: number, path: string): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestOutputsTreeActionCreator());

    const logsUrl =
      `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/${resources}/${id}/outputs/files?path=${path}`;

    return fetch(logsUrl, {
      headers: {
        'Content-Type': 'text/plain;charset=UTF-8',
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.text())
      .then((text) => dispatch(receiveOutputsFileActionCreator(text)));
  };
}
