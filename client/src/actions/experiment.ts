import { Action } from 'redux';
import * as url from 'url';

import { BASE_API_URL } from '../constants/api';
import {
  getExperimentUrl,
  getExperimentUrlFromName,
  getProjectUrl,
  getProjectUrlFromName,
  handleAuthError,
  urlifyProjectName
} from '../constants/utils';
import history from '../history';
import { BookmarkModel } from '../models/bookmark';
import { ExperimentModel } from '../models/experiment';
import { ARCHIVES, BOOKMARKS } from '../utils/endpointList';
import { fetchCodeReference } from './codeReference';

export enum actionTypes {
  CREATE_EXPERIMENT = 'CREATE_EXPERIMENT',
  DELETE_EXPERIMENT = 'DELETE_EXPERIMENT',
  DELETE_EXPERIMENTS = 'DELETE_EXPERIMENTS',
  ARCHIVE_EXPERIMENT = 'ARCHIVE_EXPERIMENT',
  RESTORE_EXPERIMENT = 'RESTORE_EXPERIMENT',
  STOP_EXPERIMENT = 'STOP_EXPERIMENT',
  STOP_EXPERIMENTS = 'STOP_EXPERIMENTS',
  UPDATE_EXPERIMENT = 'UPDATE_EXPERIMENT',
  RECEIVE_EXPERIMENT = 'RECEIVE_EXPERIMENT',
  RECEIVE_EXPERIMENTS = 'RECEIVE_EXPERIMENTS',
  RECEIVE_EXPERIMENTS_PARAMS = 'RECEIVE_EXPERIMENTS_PARAMS',
  REQUEST_EXPERIMENTS = 'REQUEST_EXPERIMENTS',
  BOOKMARK_EXPERIMENT = 'BOOKMARK_EXPERIMENT',
  UNBOOKMARK_EXPERIMENT = 'UNBOOKMARK_EXPERIMENT',
  START_EXPERIMENT_TENSORBOARD = 'START_EXPERIMENT_TENSORBOARD',
  STOP_EXPERIMENT_TENSORBOARD = 'STOP_EXPERIMENT_TENSORBOARD'
}

export interface CreateUpdateReceiveExperimentAction extends Action {
  type: actionTypes.CREATE_EXPERIMENT | actionTypes.UPDATE_EXPERIMENT | actionTypes.RECEIVE_EXPERIMENT;
  experiment: ExperimentModel;
}

export interface DeleteExperimentAction extends Action {
  type: actionTypes.DELETE_EXPERIMENT;
  experimentName: string;
}

export interface DeleteExperimentsAction extends Action {
  type: actionTypes.DELETE_EXPERIMENTS;
  projectName: string;
  experimentIds: number[];
}

export interface ArchiveExperimentAction extends Action {
  type: actionTypes.ARCHIVE_EXPERIMENT;
  experimentName: string;
}

export interface RestoreExperimentAction extends Action {
  type: actionTypes.RESTORE_EXPERIMENT;
  experimentName: string;
}

export interface StopExperimentAction extends Action {
  type: actionTypes.STOP_EXPERIMENT;
  experimentName: string;
}

export interface StopExperimentsAction extends Action {
  type: actionTypes.STOP_EXPERIMENTS;
  projectName: string;
  experimentIds: number[];
}

export interface ReceiveExperimentsAction extends Action {
  type: actionTypes.RECEIVE_EXPERIMENTS;
  experiments: ExperimentModel[];
  count: number;
}

export interface ReceiveExperimentsParamsAction extends Action {
  type: actionTypes.RECEIVE_EXPERIMENTS_PARAMS;
  experiments: ExperimentModel[];
  count: number;
}

export interface RequestExperimentsAction extends Action {
  type: actionTypes.REQUEST_EXPERIMENTS;
}

export interface BookmarkExperimentAction extends Action {
  type: actionTypes.BOOKMARK_EXPERIMENT | actionTypes.UNBOOKMARK_EXPERIMENT;
  experimentName: string;
}

export interface ExperimentTensorboardAction extends Action {
  type: actionTypes.START_EXPERIMENT_TENSORBOARD | actionTypes.STOP_EXPERIMENT_TENSORBOARD;
  experimentName: string;
}

export type ExperimentAction =
  CreateUpdateReceiveExperimentAction
  | DeleteExperimentAction
  | DeleteExperimentsAction
  | ArchiveExperimentAction
  | RestoreExperimentAction
  | StopExperimentAction
  | StopExperimentsAction
  | ReceiveExperimentsAction
  | ReceiveExperimentsParamsAction
  | RequestExperimentsAction
  | BookmarkExperimentAction
  | ExperimentTensorboardAction;

export function createExperimentActionCreator(experiment: ExperimentModel): CreateUpdateReceiveExperimentAction {
  return {
    type: actionTypes.CREATE_EXPERIMENT,
    experiment
  };
}

export function updateExperimentActionCreator(experiment: ExperimentModel): CreateUpdateReceiveExperimentAction {
  return {
    type: actionTypes.UPDATE_EXPERIMENT,
    experiment
  };
}

export function deleteExperimentActionCreator(experimentName: string): DeleteExperimentAction {
  return {
    type: actionTypes.DELETE_EXPERIMENT,
    experimentName,
  };
}

export function deleteExperimentsActionCreator(projectName: string, experimentIds: number[]): DeleteExperimentsAction {
  return {
    type: actionTypes.DELETE_EXPERIMENTS,
    projectName,
    experimentIds,
  };
}

export function archiveExperimentActionCreator(experimentName: string): ArchiveExperimentAction {
  return {
    type: actionTypes.ARCHIVE_EXPERIMENT,
    experimentName,
  };
}

export function restoreExperimentActionCreator(experimentName: string): RestoreExperimentAction {
  return {
    type: actionTypes.RESTORE_EXPERIMENT,
    experimentName,
  };
}

export function stopExperimentActionCreator(experimentName: string): StopExperimentAction {
  return {
    type: actionTypes.STOP_EXPERIMENT,
    experimentName,
  };
}

export function stopExperimentsActionCreator(projectName: string, experimentIds: number[]): StopExperimentsAction {
  return {
    type: actionTypes.STOP_EXPERIMENTS,
    projectName,
    experimentIds,
  };
}

export function requestExperimentsActionCreator(): RequestExperimentsAction {
  return {
    type: actionTypes.REQUEST_EXPERIMENTS,
  };
}

export function receiveExperimentsActionCreator(experiments: ExperimentModel[],
                                                count: number): ReceiveExperimentsAction {
  return {
    type: actionTypes.RECEIVE_EXPERIMENTS,
    experiments,
    count
  };
}

export function receiveExperimentsParamsActionCreator(experiments: ExperimentModel[],
                                                      count: number): ReceiveExperimentsParamsAction {
  return {
    type: actionTypes.RECEIVE_EXPERIMENTS_PARAMS,
    experiments,
    count
  };
}

export function receiveBookmarkedExperimentsActionCreator(bookmarkedExperiments: BookmarkModel[],
                                                          count: number): ReceiveExperimentsAction {
  const experiments: ExperimentModel[] = [];
  for (const bookmarkedExperiment of bookmarkedExperiments) {
    experiments.push(bookmarkedExperiment.content_object as ExperimentModel);
  }
  return {
    type: actionTypes.RECEIVE_EXPERIMENTS,
    experiments,
    count
  };
}

export function receiveExperimentActionCreator(experiment: ExperimentModel): CreateUpdateReceiveExperimentAction {
  return {
    type: actionTypes.RECEIVE_EXPERIMENT,
    experiment
  };
}

export function bookmarkExperimentActionCreator(experimentName: string) {
  return {
    type: actionTypes.BOOKMARK_EXPERIMENT,
    experimentName,
  };
}

export function unbookmarkExperimentActionCreator(experimentName: string) {
  return {
    type: actionTypes.UNBOOKMARK_EXPERIMENT,
    experimentName,
  };
}

export function startExperimentTensorboardActionCreator(experimentName: string) {
  return {
    type: actionTypes.START_EXPERIMENT_TENSORBOARD,
    experimentName,
  };
}

export function stopExperimentTensorboardActionCreator(experimentName: string) {
  return {
    type: actionTypes.STOP_EXPERIMENT_TENSORBOARD,
    experimentName,
  };
}

function _fetchExperiments(experimentsUrl: string,
                           endpointList: string,
                           filters: { [key: string]: number | boolean | string } = {},
                           dispatch: any,
                           getState: any,
                           updateHistory: boolean = true): any {
  dispatch(requestExperimentsActionCreator());
  const urlPieces = location.hash.split('?');
  const baseUrl = urlPieces[0];
  if (Object.keys(filters).length) {
    experimentsUrl += url.format({query: filters});
    if (baseUrl && updateHistory) {
      history.push(baseUrl + url.format({query: filters}));
    }
  } else if (urlPieces.length > 1 && updateHistory) {
    history.push(baseUrl);
  }

  const dispatchActionCreator = (results: any, count: number) => {
    if (filters && filters.declarations) {
      return dispatch(receiveExperimentsParamsActionCreator(results, count));
    }
    if (endpointList === BOOKMARKS) {
      dispatch(receiveBookmarkedExperimentsActionCreator(results, count));
    } else {
      dispatch(receiveExperimentsActionCreator(results, count));
    }
  };

  return fetch(experimentsUrl, {
    headers: {
      Authorization: 'token ' + getState().auth.token
    }
  })
    .then((response) => handleAuthError(response, dispatch))
    .then((response) => response.json())
    .then((json) => dispatchActionCreator(json.results, json.count));
}

export function fetchBookmarkedExperiments(user: string,
                                           filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const experimentsUrl = `${BASE_API_URL}/bookmarks/${user}/experiments/`;
    return _fetchExperiments(experimentsUrl, BOOKMARKS, filters, dispatch, getState);
  };
}

export function fetchArchivedExperiments(user: string,
                                         filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const experimentsUrl = `${BASE_API_URL}/archives/${user}/experiments/`;
    return _fetchExperiments(experimentsUrl, ARCHIVES, filters, dispatch, getState);
  };
}

export function fetchExperiments(projectUniqueName: string,
                                 filters: { [key: string]: number | boolean | string } = {},
                                 updateHistory: boolean = true): any {
  return (dispatch: any, getState: any) => {
    const experimentsUrl = `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/experiments/`;
    return _fetchExperiments(experimentsUrl, '', filters, dispatch, getState, updateHistory);
  };
}

export function fetchExperiment(user: string, projectName: string, experimentId: number): any {
  const experimentUrl = getExperimentUrl(user, projectName, experimentId, false);
  return (dispatch: any, getState: any) => {
    dispatch(requestExperimentsActionCreator());
    return fetch(`${BASE_API_URL}${experimentUrl}`, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.json())
      .then((json) => dispatch(receiveExperimentActionCreator(json)));
  };
}

export function deleteExperiment(experimentName: string, redirect: boolean = false): any {
  const experimentUrl = getExperimentUrlFromName(experimentName, false);
  return (dispatch: any, getState: any) => {
    return fetch(`${BASE_API_URL}${experimentUrl}`, {
      method: 'DELETE',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => {
        const dispatched = dispatch(deleteExperimentActionCreator(experimentName));
        if (redirect) {
          const values = experimentName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#experiments');
        }
        return dispatched;
      });
  };
}

export function deleteExperiments(projectName: string, experimentIds: number[]): any {
  const projectUrl = getProjectUrlFromName(projectName, false);
  return (dispatch: any, getState: any) => {
    return fetch(`${BASE_API_URL}${projectUrl}/experiments/delete`, {
      method: 'DELETE',
      body: JSON.stringify({ids: experimentIds}),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => {
        return dispatch(deleteExperimentsActionCreator(projectName, experimentIds));
      });
  };
}

export function updateExperiment(experimentName: string, updateDict: { [key: string]: any }): any {
  const experimentUrl = getExperimentUrlFromName(experimentName, false);
  return (dispatch: any, getState: any) => {
    return fetch(`${BASE_API_URL}${experimentUrl}`, {
      method: 'PATCH',
      body: JSON.stringify(updateDict),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.json())
      .then((json) => dispatch(updateExperimentActionCreator(json)));
  };
}

export function archiveExperiment(experimentName: string, redirect: boolean = false): any {
  const experimentUrl = getExperimentUrlFromName(experimentName, false);
  return (dispatch: any, getState: any) => {
    return fetch(`${BASE_API_URL}${experimentUrl}/archive`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => {
        const dispatched = dispatch(archiveExperimentActionCreator(experimentName));
        if (redirect) {
          const values = experimentName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#experiments');
        }
        return dispatched;
      });
  };
}

export function restoreExperiment(experimentName: string): any {
  const experimentUrl = getExperimentUrlFromName(experimentName, false);
  return (dispatch: any, getState: any) => {
    return fetch(`${BASE_API_URL}${experimentUrl}/restore`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(restoreExperimentActionCreator(experimentName)));
  };
}

export function stopExperiment(experimentName: string): any {
  const experimentUrl = getExperimentUrlFromName(experimentName, false);
  return (dispatch: any, getState: any) => {
    return fetch(`${BASE_API_URL}${experimentUrl}/stop`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(stopExperimentActionCreator(experimentName)));
  };
}

export function stopExperiments(projectName: string, experimentIds: number[]): any {
  const projecttUrl = getProjectUrlFromName(projectName, false);
  return (dispatch: any, getState: any) => {
    return fetch(`${BASE_API_URL}${projecttUrl}/experiments/stop`, {
      method: 'POST',
      body: JSON.stringify({ids: experimentIds}),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(stopExperimentsActionCreator(projectName, experimentIds)));
  };
}

export function bookmark(experimentName: string): any {
  const experimentUrl = getExperimentUrlFromName(experimentName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${experimentUrl}/bookmark`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(bookmarkExperimentActionCreator(experimentName)));
  };
}

export function unbookmark(experimentName: string): any {
  const experimentUrl = getExperimentUrlFromName(experimentName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${experimentUrl}/unbookmark`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(unbookmarkExperimentActionCreator(experimentName)));
  };
}

export function fetchExperimentCodeReference(experimentName: string): any {
  const experimentUrl = getExperimentUrlFromName(experimentName, false);
  const codeRefUrl = `${experimentUrl}/coderef`;
  return fetchCodeReference(codeRefUrl);
}

export function startTensorboard(experimentName: string): any {
  const experimentUrl = getExperimentUrlFromName(experimentName, false);
  return (dispatch: any, getState: any) => {
    return fetch(`${BASE_API_URL}${experimentUrl}/tensorboard/start`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(startExperimentTensorboardActionCreator(experimentName)));
  };
}

export function stopTensorboard(experimentName: string): any {
  const experimentUrl = getExperimentUrlFromName(experimentName, false);
  return (dispatch: any, getState: any) => {
    return fetch(`${BASE_API_URL}${experimentUrl}/tensorboard/stop`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(stopExperimentTensorboardActionCreator(experimentName)));
  };
}
