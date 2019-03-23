import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getExperimentUrlFromName, getProjectUrlFromName } from '../../constants/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface StopExperimentRequestAction extends Action {
  type: actionTypes.STOP_EXPERIMENT_REQUEST;
  experimentName: string;
}

export interface StopExperimentSuccessAction extends Action {
  type: actionTypes.STOP_EXPERIMENT_SUCCESS;
  experimentName: string;
}

export interface StopExperimentErrorAction extends Action {
  type: actionTypes.STOP_EXPERIMENT_ERROR;
  statusCode: number;
  error: any;
  experimentName: string;
}

export function stopExperimentRequestActionCreator(experimentName: string): StopExperimentRequestAction {
  return {
    type: actionTypes.STOP_EXPERIMENT_REQUEST,
    experimentName,
  };
}

export function stopExperimentSuccessActionCreator(experimentName: string): StopExperimentSuccessAction {
  return {
    type: actionTypes.STOP_EXPERIMENT_SUCCESS,
    experimentName,
  };
}

export function stopExperimentErrorActionCreator(statusCode: number,
                                                 error: any,
                                                 experimentName: string): StopExperimentErrorAction {
  return {
    type: actionTypes.STOP_EXPERIMENT_ERROR,
    statusCode,
    error,
    experimentName,
  };
}

export interface StopExperimentsRequestAction extends Action {
  type: actionTypes.STOP_EXPERIMENTS_REQUEST;
  projectName: string;
}

export interface StopExperimentsSuccessAction extends Action {
  type: actionTypes.STOP_EXPERIMENTS_SUCCESS;
  projectName: string;
  experimentIds: number[];
}

export interface StopExperimentsErrorAction extends Action {
  type: actionTypes.STOP_EXPERIMENTS_ERROR;
  statusCode: number;
  error: any;
  projectName: string;
}

export function stopExperimentsRequestActionCreator(projectName: string): StopExperimentsRequestAction {
  return {
    type: actionTypes.STOP_EXPERIMENTS_REQUEST,
    projectName,
  };
}

export function stopExperimentsSuccessActionCreator(projectName: string,
                                                    experimentIds: number[]): StopExperimentsSuccessAction {
  return {
    type: actionTypes.STOP_EXPERIMENTS_SUCCESS,
    projectName,
    experimentIds,
  };
}

export function stopExperimentsErrorActionCreator(statusCode: number,
                                                  error: any,
                                                  projectName: string): StopExperimentsErrorAction {
  return {
    type: actionTypes.STOP_EXPERIMENTS_ERROR,
    statusCode,
    error,
    projectName,
  };
}

export type StopExperimentAction =
  StopExperimentRequestAction
  | StopExperimentSuccessAction
  | StopExperimentErrorAction
  | StopExperimentsRequestAction
  | StopExperimentsSuccessAction
  | StopExperimentsErrorAction;

export function stopExperiment(experimentName: string): any {
  return (dispatch: any, getState: any) => {
    const experimentUrl = getExperimentUrlFromName(experimentName, false);

    dispatch(stopExperimentRequestActionCreator(experimentName));

    return fetch(`${BASE_API_URL}${experimentUrl}/stop`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        stopExperimentErrorActionCreator,
        'Experiment not found',
        'Failed to stop experiment',
        [experimentName]))
      .then(() => dispatch(stopExperimentSuccessActionCreator(experimentName)));
  };
}

export function stopExperiments(projectName: string, experimentIds: number[]): any {
  return (dispatch: any, getState: any) => {
    const projecttUrl = getProjectUrlFromName(projectName, false);

    dispatch(stopExperimentsRequestActionCreator(projectName));

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
      .then((response) => stdHandleError(
        response,
        dispatch,
        stopExperimentsErrorActionCreator,
        'Project not found',
        'Failed to stop experiments',
        [projectName]))
      .then(() => dispatch(stopExperimentsSuccessActionCreator(projectName, experimentIds)));
  };
}
