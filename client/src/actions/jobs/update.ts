import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { JobModel } from '../../models/job';
import { getJobUrlFromName } from '../../urls/utils';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface UpdateJobRequestAction extends Action {
  type: actionTypes.UPDATE_JOB_REQUEST;
  jobName: string;
}

export interface UpdateJobSuccessAction extends Action {
  type: actionTypes.UPDATE_JOB_SUCCESS;
  job: JobModel;
  jobName: string;
}

export interface UpdateJobErrorAction extends Action {
  type: actionTypes.UPDATE_JOB_ERROR;
  statusCode: number;
  error: any;
  jobName: string;
}

export function updateJobRequestActionCreator(jobName: string): UpdateJobRequestAction {
  return {
    type: actionTypes.UPDATE_JOB_REQUEST,
    jobName
  };
}

export function updateJobSuccessActionCreator(job: JobModel): UpdateJobSuccessAction {
  return {
    type: actionTypes.UPDATE_JOB_SUCCESS,
    job,
    jobName: job.unique_name
  };
}

export function updateJobErrorActionCreator(statusCode: number,
                                            error: any,
                                            jobName: string): UpdateJobErrorAction {
  return {
    type: actionTypes.UPDATE_JOB_ERROR,
    statusCode,
    error,
    jobName
  };
}

export type UpdateJobAction =
  UpdateJobRequestAction
  | UpdateJobSuccessAction
  | UpdateJobErrorAction;

export function updateJob(jobName: string, updateDict: { [key: string]: any }): any {
  return (dispatch: any, getState: any) => {
    const jobUrl = getJobUrlFromName(jobName, false);

    dispatch(updateJobRequestActionCreator(jobName));

    fetch(
      `${BASE_API_URL}${jobUrl}`, {
        method: 'PATCH',
        body: JSON.stringify(updateDict),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdCreateHandleError(
        response,
        dispatch,
        updateJobErrorActionCreator,
        'Job not found',
        'Failed to update job',
        [jobName]))
      .then((response) => response.json())
      .then((json) => dispatch(updateJobSuccessActionCreator(json)))
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(updateJobErrorActionCreator(response.status, value, jobName)));
        } else {
          return dispatch(updateJobErrorActionCreator(response.status, response.value, jobName));
        }
      });
  };
}
