import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import {
  getExperimentUniqueName,
  getExperimentUrl,
  getExperimentUrlFromName,
  getTensorboardApiUrlFromName
} from '../../constants/utils';
import history from '../../history';
import { TensorboardModel } from '../../models/tensorboard';
import { getTensorboardSuccessActionCreator } from '../tensorboards';
import { stdCreateHandleError, stdHandleError } from '../utils';
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

export function startTensorboard(user: string,
                                 projectName: string,
                                 experimentId: string,
                                 tensorboard: TensorboardModel,
                                 redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const experimentName = getExperimentUniqueName(user, projectName, experimentId);
    const experimentUrl = getExperimentUrl(user, projectName, experimentId, false);

    dispatch(startExperimentTensorboardRequestActionCreator(experimentName));

    return fetch(`${BASE_API_URL}${experimentUrl}/tensorboard/start`, {
      method: 'POST',
      body: JSON.stringify(tensorboard),
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdCreateHandleError(
        response,
        dispatch,
        startExperimentTensorboardErrorActionCreator,
        'Experiment not found',
        'Failed to start tensorboard for experiment',
        [experimentName]))
      .then((response) => response.json())
      .then((json) => {
        dispatch(startExperimentTensorboardSuccessActionCreator(experimentName));
        const dispatched = dispatch(getTensorboardSuccessActionCreator(json));
        if (redirect) {
          history.push(getTensorboardApiUrlFromName(json.unique_name, true));
        }
        return dispatched;
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(startExperimentTensorboardErrorActionCreator(
              response.status, value, experimentName)));
        } else {
          return response.value;
        }
      });
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
