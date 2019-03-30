import { Action } from 'redux';
import * as url from 'url';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { ProjectModel } from '../../models/project';
import { stdFetchHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface FetchProjectsNamesRequestAction extends Action {
  type: actionTypes.FETCH_PROJECTS_NAMES_REQUEST;
}

export interface FetchProjectsNamesSuccessAction extends Action {
  type: actionTypes.FETCH_PROJECTS_NAMES_SUCCESS;
  projects: ProjectModel[];
  count: number;
}

export interface FetchProjectsNamesErrorAction extends Action {
  type: actionTypes.FETCH_PROJECTS_NAMES_ERROR;
  statusCode: number;
  error: any;
}

export function fetchProjectsNamesRequestActionCreator(): FetchProjectsNamesRequestAction {
  return {
    type: actionTypes.FETCH_PROJECTS_NAMES_REQUEST,
  };
}

export function fetchProjectsNamesSuccessActionCreator(projects: ProjectModel[],
                                                       count: number): FetchProjectsNamesSuccessAction {
  return {
    type: actionTypes.FETCH_PROJECTS_NAMES_SUCCESS,
    projects,
    count,
  };
}

export function fetchProjectsNamesErrorActionCreator(statusCode: number, error: any): FetchProjectsNamesErrorAction {
  return {
    type: actionTypes.FETCH_PROJECTS_NAMES_ERROR,
    statusCode,
    error,
  };
}

export type FetchProjectNameAction =
  FetchProjectsNamesRequestAction
  | FetchProjectsNamesSuccessAction
  | FetchProjectsNamesErrorAction;

function _fetchProjectsNames(projectsUrl: string,
                             endpointList: string,
                             filters: { [key: string]: number | boolean | string } = {},
                             dispatch: any,
                             getState: any): any {

  dispatch(fetchProjectsNamesRequestActionCreator());

  const urlPieces = location.hash.split('?');
  const baseUrl = urlPieces[0];
  if (Object.keys(filters).length) {
    projectsUrl += url.format({query: filters});
    if (baseUrl) {
      history.push(baseUrl + url.format({query: filters}));
    }
  } else if (urlPieces.length > 1) {
    history.push(baseUrl);
  }

  const dispatchActionCreator = (results: any, count: number) => {
    return dispatch(fetchProjectsNamesSuccessActionCreator(results, count));
  };

  return fetch(projectsUrl, {
    headers: {
      Authorization: 'token ' + getState().auth.token
    }
  })
    .then((response) => stdFetchHandleError(
      response,
      dispatch,
      fetchProjectsNamesErrorActionCreator,
      'Projects not found',
      'Failed to fetch projects'))
    .then((response) => response.json())
    .then((json) => dispatchActionCreator(json.results, json.count))
    .catch((error) => undefined)
    .catch((response) => {
      if (response.status === 400) {
        return response.value.json().then(
          (value: any) => dispatch(fetchProjectsNamesErrorActionCreator(response.status, value)));
      } else {
        return response.value;
      }
    });
}

export function fetchProjectsNames(user: string,
                                   filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const projectsUrl = `${BASE_API_URL}/${user}/projects/names`;

    return _fetchProjectsNames(projectsUrl, '', filters, dispatch, getState);
  };
}
