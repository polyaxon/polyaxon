import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getJobUrlFromName } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface StopJobRequestAction extends Action {
  type: actionTypes.STOP_JOB_REQUEST;
  jobName: string;
}

export interface StopJobSuccessAction extends Action {
  type: actionTypes.STOP_JOB_SUCCESS;
  jobName: string;
}

export interface StopJobErrorAction extends Action {
  type: actionTypes.STOP_JOB_ERROR;
  statusCode: number;
  error: any;
  jobName: string;
}

export function stopJobRequestActionCreator(jobName: string): StopJobRequestAction {
  return {
    type: actionTypes.STOP_JOB_REQUEST,
    jobName
  };
}

export function stopJobSuccessActionCreator(jobName: string): StopJobSuccessAction {
  return {
    type: actionTypes.STOP_JOB_SUCCESS,
    jobName
  };
}

export function stopJobErrorActionCreator(statusCode: number,
                                          error: any,
                                          jobName: string): StopJobErrorAction {
  return {
    type: actionTypes.STOP_JOB_ERROR,
    statusCode,
    error,
    jobName
  };
}

export type StopJobAction =
  StopJobRequestAction
  | StopJobSuccessAction
  | StopJobErrorAction;

export function stopJob(jobName: string): any {
  return (dispatch: any, getState: any) => {
    const jobUrl = getJobUrlFromName(jobName, false);

    dispatch(stopJobRequestActionCreator(jobName));

    return fetch(
      `${BASE_API_URL}${jobUrl}/stop`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        stopJobErrorActionCreator,
        'Job not found',
        'Failed to stop job',
        [jobName]))
      .then(() => dispatch(stopJobSuccessActionCreator(jobName)));
  };
}
