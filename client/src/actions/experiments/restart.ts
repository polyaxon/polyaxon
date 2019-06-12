import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { getExperimentUrlFromName } from '../../urls/utils';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';
import { getExperimentSuccessActionCreator } from './get';

export interface RestartExperimentRequestAction extends Action {
  type: actionTypes.RESTART_EXPERIMENT_REQUEST;
  experimentName: string;
}

export interface RestartExperimentSuccessAction extends Action {
  type: actionTypes.RESTART_EXPERIMENT_SUCCESS;
  experimentName: string;
}

export interface RestartExperimentErrorAction extends Action {
  type: actionTypes.RESTART_EXPERIMENT_ERROR;
  statusCode: number;
  error: any;
  experimentName: string;
}

export function restartExperimentRequestActionCreator(experimentName: string): RestartExperimentRequestAction {
  return {
    type: actionTypes.RESTART_EXPERIMENT_REQUEST,
    experimentName,
  };
}

export function restartExperimentSuccessActionCreator(experimentName: string): RestartExperimentSuccessAction {
  return {
    type: actionTypes.RESTART_EXPERIMENT_SUCCESS,
    experimentName,
  };
}

export function restartExperimentErrorActionCreator(statusCode: number,
                                                    error: any,
                                                    experimentName: string): RestartExperimentErrorAction {
  return {
    type: actionTypes.RESTART_EXPERIMENT_ERROR,
    statusCode,
    error,
    experimentName,
  };
}

export type RestartExperimentAction =
  RestartExperimentRequestAction
  | RestartExperimentSuccessAction
  | RestartExperimentErrorAction;

export function restartExperiment(experimentName: string, redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const experimentUrl = getExperimentUrlFromName(experimentName, false);

    dispatch(restartExperimentRequestActionCreator(experimentName));

    return fetch(`${BASE_API_URL}${experimentUrl}/restart`, {
      method: 'POST',
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
        restartExperimentErrorActionCreator,
        'Not found',
        'Failed to restart experiment',
        [experimentName]))
      .then((response) => response.json())
      .then((json) => {
        restartExperimentSuccessActionCreator(experimentName);
        const dispatched = dispatch(getExperimentSuccessActionCreator(json));
        if (redirect) {
          history.push(getExperimentUrlFromName( json.unique_name, true));
        }
        return dispatched;
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(restartExperimentErrorActionCreator(response.status, value, experimentName)));
        } else {
          return response.value;
        }
      });
  };
}
