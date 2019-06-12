import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { getJobUrlFromName } from '../../urls/utils';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';
import { getJobSuccessActionCreator } from './get';

export interface RestartJobRequestAction extends Action {
  type: actionTypes.RESTART_JOB_REQUEST;
  jobName: string;
}

export interface RestartJobSuccessAction extends Action {
  type: actionTypes.RESTART_JOB_SUCCESS;
  jobName: string;
}

export interface RestartJobErrorAction extends Action {
  type: actionTypes.RESTART_JOB_ERROR;
  statusCode: number;
  error: any;
  jobName: string;
}

export function restartJobRequestActionCreator(jobName: string): RestartJobRequestAction {
  return {
    type: actionTypes.RESTART_JOB_REQUEST,
    jobName
  };
}

export function restartJobSuccessActionCreator(jobName: string): RestartJobSuccessAction {
  return {
    type: actionTypes.RESTART_JOB_SUCCESS,
    jobName
  };
}

export function restartJobErrorActionCreator(statusCode: number,
                                             error: any,
                                             jobName: string): RestartJobErrorAction {
  return {
    type: actionTypes.RESTART_JOB_ERROR,
    statusCode,
    error,
    jobName
  };
}

export type RestartJobAction =
  RestartJobRequestAction
  | RestartJobSuccessAction
  | RestartJobErrorAction;

export function restartJob(jobName: string, redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const jobUrl = getJobUrlFromName(jobName, false);

    dispatch(restartJobRequestActionCreator(jobName));

    return fetch(`${BASE_API_URL}${jobUrl}/restart`, {
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
        restartJobErrorActionCreator,
        'Not found',
        'Failed to restart job',
        [jobName]))
      .then((response) => response.json())
      .then((json) => {
        restartJobSuccessActionCreator(jobName);
        const dispatched = dispatch(getJobSuccessActionCreator(json));
        if (redirect) {
          history.push(getJobUrlFromName( json.unique_name, true));
        }
        return dispatched;
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(restartJobErrorActionCreator(response.status, value, jobName)));
        } else {
          return response.value;
        }
      });
  };
}
