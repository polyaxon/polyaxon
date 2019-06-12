import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getJobUrlFromName } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface RestoreJobRequestAction extends Action {
  type: actionTypes.RESTORE_JOB_REQUEST;
  jobName: string;
}

export interface RestoreJobSuccessAction extends Action {
  type: actionTypes.RESTORE_JOB_SUCCESS;
  jobName: string;
}

export interface RestoreJobErrorAction extends Action {
  type: actionTypes.RESTORE_JOB_ERROR;
  statusCode: number;
  error: any;
  jobName: string;
}

export function restoreJobRequestActionCreator(jobName: string): RestoreJobRequestAction {
  return {
    type: actionTypes.RESTORE_JOB_REQUEST,
    jobName
  };
}

export function restoreJobSuccessActionCreator(jobName: string): RestoreJobSuccessAction {
  return {
    type: actionTypes.RESTORE_JOB_SUCCESS,
    jobName
  };
}

export function restoreJobErrorActionCreator(statusCode: number,
                                             error: any,
                                             jobName: string): RestoreJobErrorAction {
  return {
    type: actionTypes.RESTORE_JOB_ERROR,
    statusCode,
    error,
    jobName
  };
}

export type RestoreJobAction =
  RestoreJobRequestAction
  | RestoreJobSuccessAction
  | RestoreJobErrorAction;

export function restoreJob(jobName: string): any {
  return (dispatch: any, getState: any) => {
    const jobUrl = getJobUrlFromName(jobName, false);

    dispatch(restoreJobRequestActionCreator(jobName));

    return fetch(
      `${BASE_API_URL}${jobUrl}/restore`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        restoreJobErrorActionCreator,
        'Job not found',
        'Failed to restore job',
        [jobName]))
      .then(() => dispatch(restoreJobSuccessActionCreator(jobName)));
  };
}
