import { Action } from 'redux';
import * as url from 'url';

import { handleAuthError, urlifyProjectName } from '../constants/utils';
import { JobModel } from '../models/job';
import { BASE_API_URL } from '../constants/api';
import * as paginationActions from '../actions/pagination';
import { getOffset } from '../constants/paginate';

export enum actionTypes {
  CREATE_JOB = 'CREATE_JOB',
  DELETE_JOB = 'DELETE_JOB',
  UPDATE_JOB = 'UPDATE_JOB',
  RECEIVE_JOB = 'RECEIVE_JOB',
  RECEIVE_JOBS = 'RECEIVE_JOBS',
  REQUEST_JOB = 'REQUEST_JOB',
  REQUEST_JOBS = 'REQUEST_JOBS',
}

export interface CreateUpdateReceiveJobAction extends Action {
  type: actionTypes.CREATE_JOB | actionTypes.UPDATE_JOB | actionTypes.RECEIVE_JOB;
  job: JobModel;
}

export interface DeleteJobAction extends Action {
  type: actionTypes.DELETE_JOB;
  job: JobModel;
}

export interface ReceiveJobsAction extends Action {
  type: actionTypes.RECEIVE_JOBS;
  jobs: JobModel[];
}

export interface RequestJobsAction extends Action {
  type: actionTypes.REQUEST_JOBS | actionTypes.REQUEST_JOB;
}

export type JobAction =
  CreateUpdateReceiveJobAction
  | DeleteJobAction
  | ReceiveJobsAction
  | RequestJobsAction;

export function createJobActionCreator(job: JobModel): CreateUpdateReceiveJobAction {
  return {
    type: actionTypes.CREATE_JOB,
    job
  };
}

export function updateJobActionCreator(job: JobModel): CreateUpdateReceiveJobAction {
  return {
    type: actionTypes.UPDATE_JOB,
    job
  };
}

export function deleteJobActionCreator(job: JobModel): DeleteJobAction {
  return {
    type: actionTypes.DELETE_JOB,
    job
  };
}

export function requestJobActionCreator(): RequestJobsAction {
  return {
    type: actionTypes.REQUEST_JOB,
  };
}

export function requestJobsActionCreator(): RequestJobsAction {
  return {
    type: actionTypes.REQUEST_JOBS,
  };
}

export function receiveJobActionCreator(job: JobModel): CreateUpdateReceiveJobAction {
  return {
    type: actionTypes.RECEIVE_JOB,
    job
  };
}

export function receiveJobsActionCreator(jobs: JobModel[]): ReceiveJobsAction {
  return {
    type: actionTypes.RECEIVE_JOBS,
    jobs
  };
}

export function fetchJobs(projectUniqueName: string, experimentId: number, currentPage?: number): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestJobsActionCreator());
    paginationActions.paginateJob(dispatch, currentPage);
    let jobsUrl =
      BASE_API_URL + `/${urlifyProjectName(projectUniqueName)}` + '/experiments/' + experimentId + '/jobs';
    let offset = getOffset(currentPage);
    if (offset != null) {
      jobsUrl += url.format({query: {offset: offset}});
    }
    return fetch(
      jobsUrl, {
      headers: {
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then(response => handleAuthError(response, dispatch))
      .then(response => response.json())
      .then(json => json.results)
      .then(json => dispatch(receiveJobsActionCreator(json)));
  };
}

export function fetchJob(user: string, projectName: string, experimentId: number, jobId: number): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestJobActionCreator());
    return fetch(
      BASE_API_URL + `/${user}/${projectName}` + '/experiments/' + experimentId + '/jobs/' + jobId, {
      headers: {
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then(response => handleAuthError(response, dispatch))
      .then(response => response.json())
      .then(json => dispatch(receiveJobActionCreator(json)));
  };
}
