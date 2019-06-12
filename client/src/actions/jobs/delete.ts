import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { getJobUrlFromName, getProjectUrl } from '../../urls/utils';
import { stdDeleteHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface DeleteJobRequestAction extends Action {
  type: actionTypes.DELETE_JOB_REQUEST;
  jobName: string;
}

export interface DeleteJobSuccessAction extends Action {
  type: actionTypes.DELETE_JOB_SUCCESS;
  jobName: string;
}

export interface DeleteJobErrorAction extends Action {
  type: actionTypes.DELETE_JOB_ERROR;
  statusCode: number;
  error: any;
  jobName: string;
}

export function deleteJobRequestActionCreator(jobName: string): DeleteJobRequestAction {
  return {
    type: actionTypes.DELETE_JOB_REQUEST,
    jobName
  };
}

export function deleteJobSuccessActionCreator(jobName: string): DeleteJobSuccessAction {
  return {
    type: actionTypes.DELETE_JOB_SUCCESS,
    jobName
  };
}

export function deleteJobErrorActionCreator(statusCode: number,
                                            error: any,
                                            jobName: string): DeleteJobErrorAction {
  return {
    type: actionTypes.DELETE_JOB_ERROR,
    statusCode,
    error,
    jobName
  };
}

export type DeleteJobAction =
  DeleteJobRequestAction
  | DeleteJobSuccessAction
  | DeleteJobErrorAction;

export function deleteJob(jobName: string, redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const jobUrl = getJobUrlFromName(jobName, false);

    dispatch(deleteJobRequestActionCreator(jobName));

    fetch(
      `${BASE_API_URL}${jobUrl}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdDeleteHandleError(
        response,
        dispatch,
        deleteJobErrorActionCreator,
        'Job not found',
        'Failed to delete job',
        [jobName]))
      .then(() => {
        const dispatched = dispatch(deleteJobSuccessActionCreator(jobName));
        if (redirect) {
          const values = jobName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#jobs');
        }
        return dispatched;
      });
  };
}
