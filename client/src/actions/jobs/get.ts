import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getJobUniqueName, getJobUrl } from '../../constants/utils';
import { JobModel } from '../../models/job';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface GetJobRequestAction extends Action {
  type: actionTypes.GET_JOB_REQUEST;
  jobName: string;
}

export interface GetJobSuccessAction extends Action {
  type: actionTypes.GET_JOB_SUCCESS;
  job: JobModel;
  jobName: string;
}

export interface GetJobErrorAction extends Action {
  type: actionTypes.GET_JOB_ERROR;
  statusCode: number;
  error: any;
  jobName: string;
}

export function getJobRequestActionCreator(jobName: string): GetJobRequestAction {
  return {
    type: actionTypes.GET_JOB_REQUEST,
    jobName
  };
}

export function getJobSuccessActionCreator(job: JobModel): GetJobSuccessAction {
  return {
    type: actionTypes.GET_JOB_SUCCESS,
    job,
    jobName: job.unique_name
  };
}

export function getJobErrorActionCreator(statusCode: number, error: any, jobName: string): GetJobErrorAction {
  return {
    type: actionTypes.GET_JOB_ERROR,
    statusCode,
    error,
    jobName
  };
}

export type GetJobAction =
  GetJobRequestAction
  | GetJobSuccessAction
  | GetJobErrorAction;

export function fetchJob(user: string, projectName: string, jobId: number): any {
  return (dispatch: any, getState: any) => {
    const jobUrl = getJobUrl(user, projectName, jobId, false);
    const jobName = getJobUniqueName(user, projectName, jobId);

    dispatch(getJobRequestActionCreator(jobName));

    return fetch(
      `${BASE_API_URL}${jobUrl}`, {
        headers: {
          Authorization: 'token ' + getState().auth.token
        }
      })
       .then((response) => stdHandleError(
        response,
        dispatch,
        getJobErrorActionCreator,
        'Job not found',
        'Failed to fetch job',
        [jobName]))
      .then((response) => response.json())
      .then((json) => dispatch(getJobSuccessActionCreator(json)));
  };
}
