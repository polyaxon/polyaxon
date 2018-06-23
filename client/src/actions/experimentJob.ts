import { Action } from 'redux';
import * as url from 'url';

import history from '../history';
import { handleAuthError, urlifyProjectName } from '../constants/utils';
import { ExperimentJobModel } from '../models/experimentJob';
import { BASE_API_URL } from '../constants/api';

export enum actionTypes {
  CREATE_EXPERIMENT_JOB = 'CREATE_EXPERIMENT_JOB',
  DELETE_EXPERIMENT_JOB = 'DELETE_EXPERIMENT_JOB',
  UPDATE_EXPERIMENT_JOB = 'UPDATE_EXPERIMENT_JOB',
  RECEIVE_EXPERIMENT_JOB = 'RECEIVE_EXPERIMENT_JOB',
  RECEIVE_EXPERIMENT_JOBS = 'RECEIVE_EXPERIMENT_JOBS',
  REQUEST_EXPERIMENT_JOB = 'REQUEST_EXPERIMENT_JOB',
  REQUEST_EXPERIMENT_JOBS = 'REQUEST_EXPERIMENT_JOBS',
}

export interface CreateUpdateReceiveExperimentJobAction extends Action {
  type: actionTypes.CREATE_EXPERIMENT_JOB
    | actionTypes.UPDATE_EXPERIMENT_JOB
    | actionTypes.RECEIVE_EXPERIMENT_JOB;
  job: ExperimentJobModel;
}

export interface DeleteExperimentJobAction extends Action {
  type: actionTypes.DELETE_EXPERIMENT_JOB;
  job: ExperimentJobModel;
}

export interface ReceiveExperimentJobsAction extends Action {
  type: actionTypes.RECEIVE_EXPERIMENT_JOBS;
  jobs: ExperimentJobModel[];
  count: number;
}

export interface RequestExperimentJobsAction extends Action {
  type: actionTypes.REQUEST_EXPERIMENT_JOBS | actionTypes.REQUEST_EXPERIMENT_JOB;
}

export type ExperimentJobAction =
  CreateUpdateReceiveExperimentJobAction
  | DeleteExperimentJobAction
  | ReceiveExperimentJobsAction
  | RequestExperimentJobsAction;

export function createExperimentJobActionCreator(job: ExperimentJobModel): CreateUpdateReceiveExperimentJobAction {
  return {
    type: actionTypes.CREATE_EXPERIMENT_JOB,
    job
  };
}

export function updateExperimentJobActionCreator(job: ExperimentJobModel): CreateUpdateReceiveExperimentJobAction {
  return {
    type: actionTypes.UPDATE_EXPERIMENT_JOB,
    job
  };
}

export function deleteExperimentJobActionCreator(job: ExperimentJobModel): DeleteExperimentJobAction {
  return {
    type: actionTypes.DELETE_EXPERIMENT_JOB,
    job
  };
}

export function requestExperimentJobActionCreator(): RequestExperimentJobsAction {
  return {
    type: actionTypes.REQUEST_EXPERIMENT_JOB,
  };
}

export function requestExperimentJobsActionCreator(): RequestExperimentJobsAction {
  return {
    type: actionTypes.REQUEST_EXPERIMENT_JOBS,
  };
}

export function receiveExperimentJobActionCreator(job: ExperimentJobModel): CreateUpdateReceiveExperimentJobAction {
  return {
    type: actionTypes.RECEIVE_EXPERIMENT_JOB,
    job
  };
}

export function receiveExperimentJobsActionCreator(jobs: ExperimentJobModel[],
                                                   count: number): ReceiveExperimentJobsAction {
  return {
    type: actionTypes.RECEIVE_EXPERIMENT_JOBS,
    jobs,
    count
  };
}

export function fetchExperimentJobs(projectUniqueName: string,
                                    experimentId: number,
                                    filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestExperimentJobsActionCreator());
    let jobsUrl =
      BASE_API_URL + `/${urlifyProjectName(projectUniqueName)}` + '/experiments/' + experimentId + '/jobs';
    if (Object.keys(filters).length) {
      jobsUrl += url.format({query: filters});
      let baseUrl = location.hash.split('?')[0];
      if (baseUrl) {
        history.push(baseUrl + url.format({query: filters}));
      }
    }
    return fetch(
      jobsUrl, {
        headers: {
          'Authorization': 'token ' + getState().auth.token
        }
      })
      .then(response => handleAuthError(response, dispatch))
      .then(response => response.json())
      .then(json => dispatch(receiveExperimentJobsActionCreator(json.results, json.count)));
  };
}

export function fetchExperimentJob(user: string,
                                   projectName: string,
                                   experimentId: number,
                                   jobId: number): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestExperimentJobActionCreator());
    return fetch(
      BASE_API_URL + `/${user}/${projectName}` + '/experiments/' + experimentId + '/jobs/' + jobId, {
        headers: {
          'Authorization': 'token ' + getState().auth.token
        }
      })
      .then(response => handleAuthError(response, dispatch))
      .then(response => response.json())
      .then(json => dispatch(receiveExperimentJobActionCreator(json)));
  };
}
