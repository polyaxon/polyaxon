import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getExperimentUrlFromName } from '../../constants/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface StartExperimentTensorboardRequestAction extends Action {
  type: actionTypes.START_EXPERIMENT_TENSORBOARD_REQUEST;
  experimentName: string;
}

export interface StartExperimentTensorboardSuccessAction extends Action {
  type: actionTypes.START_EXPERIMENT_TENSORBOARD_SUCCESS;
  experimentName: string;
}

export interface StartExperimentTensorboardErrorAction extends Action {
  type: actionTypes.START_EXPERIMENT_TENSORBOARD_ERROR;
  statusCode: number;
  error: any;
  experimentName: string;
}

export function startExperimentTensorboardRequestActionCreator(
  experimentName: string): StartExperimentTensorboardRequestAction {
  return {
    type: actionTypes.START_EXPERIMENT_TENSORBOARD_REQUEST,
    experimentName,
  };
}

export function startExperimentTensorboardSuccessActionCreator(
  experimentName: string): StartExperimentTensorboardSuccessAction {
  return {
    type: actionTypes.START_EXPERIMENT_TENSORBOARD_SUCCESS,
    experimentName,
  };
}

export function startExperimentTensorboardErrorActionCreator(
  statusCode: number,
  error: any,
  experimentName: string): StartExperimentTensorboardErrorAction {
  return {
    type: actionTypes.START_EXPERIMENT_TENSORBOARD_ERROR,
    statusCode,
    error,
    experimentName,
  };
}

export interface StopExperimentTensorboardRequestAction extends Action {
  type: actionTypes.STOP_EXPERIMENT_TENSORBOARD_REQUEST;
  experimentName: string;
}

export interface StopExperimentTensorboardSuccessAction extends Action {
  type: actionTypes.STOP_EXPERIMENT_TENSORBOARD_SUCCESS;
  experimentName: string;
}

export interface StopExperimentTensorboardErrorAction extends Action {
  type: actionTypes.STOP_EXPERIMENT_TENSORBOARD_ERROR;
  statusCode: number;
  error: any;
  experimentName: string;
}

export function stopExperimentTensorboardRequestActionCreator(
  experimentName: string): StopExperimentTensorboardRequestAction {
  return {
    type: actionTypes.STOP_EXPERIMENT_TENSORBOARD_REQUEST,
    experimentName,
  };
}

export function stopExperimentTensorboardSuccessActionCreator(
  experimentName: string): StopExperimentTensorboardSuccessAction {
  return {
    type: actionTypes.STOP_EXPERIMENT_TENSORBOARD_SUCCESS,
    experimentName,
  };
}

export function stopExperimentTensorboardErrorActionCreator(
  statusCode: number,
  error: any,
  experimentName: string): StopExperimentTensorboardErrorAction {
  return {
    type: actionTypes.STOP_EXPERIMENT_TENSORBOARD_ERROR,
    statusCode,
    error,
    experimentName,
  };
}

export type TensorboardExperimentAction =
  StartExperimentTensorboardRequestAction
  | StartExperimentTensorboardSuccessAction
  | StartExperimentTensorboardErrorAction
  | StopExperimentTensorboardRequestAction
  | StopExperimentTensorboardSuccessAction
  | StopExperimentTensorboardErrorAction;

export function startTensorboard(experimentName: string): any {
  return (dispatch: any, getState: any) => {
    const experimentUrl = getExperimentUrlFromName(experimentName, false);

    dispatch(startExperimentTensorboardRequestActionCreator(experimentName));

    return fetch(`${BASE_API_URL}${experimentUrl}/tensorboard/start`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        startExperimentTensorboardErrorActionCreator,
        'Experiment not found',
        'Failed to start tensorboard for experiment',
        [experimentName]))
      .then(() => dispatch(startExperimentTensorboardSuccessActionCreator(experimentName)));
  };
}

export function stopTensorboard(experimentName: string): any {
  return (dispatch: any, getState: any) => {
    const experimentUrl = getExperimentUrlFromName(experimentName, false);

    dispatch(stopExperimentTensorboardRequestActionCreator(experimentName));

    return fetch(`${BASE_API_URL}${experimentUrl}/tensorboard/stop`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        stopExperimentTensorboardErrorActionCreator,
        'Experiment/Tensorboard not found',
        'Failed to stop tensorboard for experiment',
        [experimentName]))
      .then(() => dispatch(stopExperimentTensorboardSuccessActionCreator(experimentName)));
  };
}
