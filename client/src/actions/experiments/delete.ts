import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getExperimentUrlFromName, getProjectUrl, getProjectUrlFromName } from '../../constants/utils';
import history from '../../history';
import { stdDeleteHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface DeleteExperimentRequestAction extends Action {
  type: actionTypes.DELETE_EXPERIMENT_REQUEST;
  experimentName: string;
}

export interface DeleteExperimentSuccessAction extends Action {
  type: actionTypes.DELETE_EXPERIMENT_SUCCESS;
  experimentName: string;
}

export interface DeleteExperimentErrorAction extends Action {
  type: actionTypes.DELETE_EXPERIMENT_ERROR;
  statusCode: number;
  error: any;
  experimentName: string;
}

export function deleteExperimentRequestActionCreator(experimentName: string): DeleteExperimentRequestAction {
  return {
    type: actionTypes.DELETE_EXPERIMENT_REQUEST,
    experimentName,
  };
}

export function deleteExperimentSuccessActionCreator(experimentName: string): DeleteExperimentSuccessAction {
  return {
    type: actionTypes.DELETE_EXPERIMENT_SUCCESS,
    experimentName,
  };
}

export function deleteExperimentErrorActionCreator(statusCode: number,
                                                   error: any,
                                                   experimentName: string): DeleteExperimentErrorAction {
  return {
    type: actionTypes.DELETE_EXPERIMENT_ERROR,
    statusCode,
    error,
    experimentName,
  };
}

export interface DeleteExperimentsRequestAction extends Action {
  type: actionTypes.DELETE_EXPERIMENTS_REQUEST;
  projectName: string;
}

export interface DeleteExperimentsSuccessAction extends Action {
  type: actionTypes.DELETE_EXPERIMENTS_SUCCESS;
  projectName: string;
  experimentIds: number[];
}

export interface DeleteExperimentsErrorAction extends Action {
  type: actionTypes.DELETE_EXPERIMENTS_ERROR;
  statusCode: number;
  error: any;
  projectName: string;
}

export function deleteExperimentsRequestActionCreator(projectName: string): DeleteExperimentsRequestAction {
  return {
    type: actionTypes.DELETE_EXPERIMENTS_REQUEST,
    projectName
  };
}

export function deleteExperimentsSuccessActionCreator(projectName: string,
                                                      experimentIds: number[]): DeleteExperimentsSuccessAction {
  return {
    type: actionTypes.DELETE_EXPERIMENTS_SUCCESS,
    projectName,
    experimentIds,
  };
}

export function deleteExperimentsErrorActionCreator(statusCode: number,
                                                    error: any,
                                                    projectName: string): DeleteExperimentsErrorAction {
  return {
    type: actionTypes.DELETE_EXPERIMENTS_ERROR,
    statusCode,
    error,
    projectName
  };
}

export type DeleteExperimentAction =
  DeleteExperimentRequestAction
  | DeleteExperimentSuccessAction
  | DeleteExperimentErrorAction
  | DeleteExperimentsRequestAction
  | DeleteExperimentsSuccessAction
  | DeleteExperimentsErrorAction;

export function deleteExperiment(experimentName: string, redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const experimentUrl = getExperimentUrlFromName(experimentName, false);

    dispatch(deleteExperimentRequestActionCreator(experimentName));

    return fetch(`${BASE_API_URL}${experimentUrl}`, {
      method: 'DELETE',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdDeleteHandleError(
        response,
        dispatch,
        deleteExperimentErrorActionCreator,
        'Experiment not found',
        'Failed to delete experiment',
        [experimentName]))
      .then(() => {
        const dispatched = dispatch(deleteExperimentSuccessActionCreator(experimentName));
        if (redirect) {
          const values = experimentName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#experiments');
        }
        return dispatched;
      });
  };
}

export function deleteExperiments(projectName: string, experimentIds: number[]): any {
  return (dispatch: any, getState: any) => {
    const projectUrl = getProjectUrlFromName(projectName, false);

    dispatch(deleteExperimentsRequestActionCreator(projectName));

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
      .then((response) => stdDeleteHandleError(
        response,
        dispatch,
        deleteExperimentsErrorActionCreator,
        'Project not found',
        'Failed to delete experiments',
        [projectName]))
      .then(() => {
        return dispatch(deleteExperimentsSuccessActionCreator(projectName, experimentIds));
      });
  };
}
