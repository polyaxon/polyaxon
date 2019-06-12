import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { ExperimentJobModel } from '../../models/experimentJob';
import { getExperimentJobUniqueName, } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface GetExperimentJobRequestAction extends Action {
  type: actionTypes.GET_EXPERIMENT_JOB_REQUEST;
  jobName: string;
}

export interface GetExperimentJobSuccessAction extends Action {
  type: actionTypes.GET_EXPERIMENT_JOB_SUCCESS;
  job: ExperimentJobModel;
  jobName: string;
}

export interface GetExperimentJobErrorAction extends Action {
  type: actionTypes.GET_EXPERIMENT_JOB_ERROR;
  statusCode: number;
  error: any;
  jobName: string;
}

export function getExperimentJobRequestActionCreator(jobName: string): GetExperimentJobRequestAction {
  return {
    type: actionTypes.GET_EXPERIMENT_JOB_REQUEST,
    jobName
  };
}

export function getExperimentJobSuccessActionCreator(job: ExperimentJobModel): GetExperimentJobSuccessAction {
  return {
    type: actionTypes.GET_EXPERIMENT_JOB_SUCCESS,
    job,
    jobName: job.unique_name
  };
}

export function getExperimentJobErrorActionCreator(statusCode: number,
                                                   error: any,
                                                   jobName: string): GetExperimentJobErrorAction {
  return {
    type: actionTypes.GET_EXPERIMENT_JOB_ERROR,
    statusCode,
    error,
    jobName
  };
}

export type GetExperimentJobAction =
  GetExperimentJobRequestAction
  | GetExperimentJobSuccessAction
  | GetExperimentJobErrorAction;

export function fetchExperimentJob(user: string,
                                   projectName: string,
                                   experimentId: number,
                                   jobId: number): any {
  return (dispatch: any, getState: any) => {
    const experimentJobName = getExperimentJobUniqueName(user, projectName, experimentId, jobId);

    dispatch(getExperimentJobRequestActionCreator(experimentJobName));

    return fetch(
      `${BASE_API_URL}/${user}/${projectName}/experiments/${experimentId}/jobs/${jobId}`, {
        headers: {
          Authorization: 'token ' + getState().auth.token
        }
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        getExperimentJobErrorActionCreator,
        'Experiment job not found',
        'Failed to fetch experiment job',
        [experimentJobName]))
      .then((response) => response.json())
      .then((json) => dispatch(getExperimentJobSuccessActionCreator(json)));
  };
}
