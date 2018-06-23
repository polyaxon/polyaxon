import { Action } from 'redux';
import * as url from 'url';

import history from '../history';
import { handleAuthError, urlifyProjectName } from '../constants/utils';
import { BuildModel } from '../models/build';
import { BASE_API_URL } from '../constants/api';

export enum actionTypes {
  CREATE_BUILD = 'CREATE_BUILD',
  DELETE_BUILD = 'DELETE_BUILD',
  UPDATE_BUILD = 'UPDATE_BUILD',
  RECEIVE_BUILD = 'RECEIVE_BUILD',
  RECEIVE_BUILDS = 'RECEIVE_BUILDS',
  REQUEST_BUILD = 'REQUEST_BUILD',
  REQUEST_BUILDS = 'REQUEST_BUILDS',
}

export interface CreateUpdateReceiveBuildAction extends Action {
  type: actionTypes.CREATE_BUILD | actionTypes.UPDATE_BUILD | actionTypes.RECEIVE_BUILD;
  build: BuildModel;
}

export interface DeleteBuildAction extends Action {
  type: actionTypes.DELETE_BUILD;
  build: BuildModel;
}

export interface ReceiveBuildsAction extends Action {
  type: actionTypes.RECEIVE_BUILDS;
  builds: BuildModel[];
  count: number;
}

export interface RequestBuildsAction extends Action {
  type: actionTypes.REQUEST_BUILDS | actionTypes.REQUEST_BUILD;
}

export type BuildAction =
  CreateUpdateReceiveBuildAction
  | DeleteBuildAction
  | ReceiveBuildsAction
  | RequestBuildsAction;

export function createBuildActionCreator(build: BuildModel): CreateUpdateReceiveBuildAction {
  return {
    type: actionTypes.CREATE_BUILD,
    build
  };
}

export function updateBuildActionCreator(build: BuildModel): CreateUpdateReceiveBuildAction {
  return {
    type: actionTypes.UPDATE_BUILD,
    build
  };
}

export function deleteBuildActionCreator(build: BuildModel): DeleteBuildAction {
  return {
    type: actionTypes.DELETE_BUILD,
    build
  };
}

export function requestBuildActionCreator(): RequestBuildsAction {
  return {
    type: actionTypes.REQUEST_BUILD,
  };
}

export function requestBuildsActionCreator(): RequestBuildsAction {
  return {
    type: actionTypes.REQUEST_BUILDS,
  };
}

export function receiveBuildActionCreator(build: BuildModel): CreateUpdateReceiveBuildAction {
  return {
    type: actionTypes.RECEIVE_BUILD,
    build
  };
}

export function receiveBuildsActionCreator(builds: BuildModel[], count: number): ReceiveBuildsAction {
  return {
    type: actionTypes.RECEIVE_BUILDS,
    builds,
    count
  };
}

export function fetchBuilds(projectUniqueName: string,
                            filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestBuildsActionCreator());
    let buildsUrl = BASE_API_URL + `/${urlifyProjectName(projectUniqueName)}` + '/builds';
    if (Object.keys(filters).length) {
      buildsUrl += url.format({query: filters});
      let baseUrl = location.hash.split('?')[0];
      if (baseUrl) {
        history.push(baseUrl + url.format({query: filters}));
      }
    }
    return fetch(
      buildsUrl, {
        headers: {
          'Authorization': 'token ' + getState().auth.token
        }
      })
      .then(response => handleAuthError(response, dispatch))
      .then(response => response.json())
      .then(json => dispatch(receiveBuildsActionCreator(json.results, json.count)));
  };
}

export function fetchBuild(user: string, projectName: string, buildId: number): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestBuildActionCreator());
    return fetch(
      BASE_API_URL + `/${user}/${projectName}` + '/builds/' + buildId, {
        headers: {
          'Authorization': 'token ' + getState().auth.token
        }
      })
      .then(response => handleAuthError(response, dispatch))
      .then(response => response.json())
      .then(json => dispatch(receiveBuildActionCreator(json)));
  };
}
