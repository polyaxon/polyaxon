import { Action } from 'redux';
import * as url from 'url';

import { handleAuthError, urlifyProjectName } from '../constants/utils';
import { BuildModel } from '../models/build';
import { BASE_API_URL } from '../constants/api';
import * as paginationActions from '../actions/pagination';
import { getOffset } from '../constants/paginate';

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

export function receiveBuildsActionCreator(builds: BuildModel[]): ReceiveBuildsAction {
  return {
    type: actionTypes.RECEIVE_BUILDS,
    builds
  };
}

export function fetchBuilds(projectUniqueName: string, currentPage?: number): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestBuildsActionCreator());
    paginationActions.paginateBuild(dispatch, currentPage);
    let buildsUrl = BASE_API_URL + `/${urlifyProjectName(projectUniqueName)}` + '/builds';
    let offset = getOffset(currentPage);
    if (offset != null) {
      buildsUrl += url.format({query: {offset: offset}});
    }
    return fetch(
      buildsUrl, {
      headers: {
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then(response => handleAuthError(response, dispatch))
      .then(response => response.json())
      .then(json => json.results)
      .then(json => dispatch(receiveBuildsActionCreator(json)));
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
