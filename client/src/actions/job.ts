import { Action } from 'redux';
import * as url from 'url';

import { BASE_API_URL } from '../constants/api';
import {
  getJobUniqueName,
  getJobUrl,
  handleAuthError,
  urlifyProjectName
} from '../constants/utils';
import history from '../history';
import { BookmarkModel } from '../models/bookmark';
import { JobModel } from '../models/job';

export enum actionTypes {
  CREATE_JOB = 'CREATE_JOB',
  DELETE_JOB = 'DELETE_JOB',
  UPDATE_JOB = 'UPDATE_JOB',
  RECEIVE_JOB = 'RECEIVE_JOB',
  RECEIVE_JOBS = 'RECEIVE_JOBS',
  REQUEST_JOB = 'REQUEST_JOB',
  REQUEST_JOBS = 'REQUEST_JOBS',
  BOOKMARK_JOB = 'BOOKMARK_JOB',
  UNBOOKMARK_JOB = 'UNBOOKMARK_JOB',
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
  count: number;
}

export interface RequestJobsAction extends Action {
  type: actionTypes.REQUEST_JOBS | actionTypes.REQUEST_JOB;
}

export interface BookmarkJobAction extends Action {
  type: actionTypes.BOOKMARK_JOB | actionTypes.UNBOOKMARK_JOB;
  jobName: string;
}

export type JobAction =
  CreateUpdateReceiveJobAction
  | DeleteJobAction
  | ReceiveJobsAction
  | RequestJobsAction
  | BookmarkJobAction;

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

export function receiveJobsActionCreator(jobs: JobModel[], count: number): ReceiveJobsAction {
  return {
    type: actionTypes.RECEIVE_JOBS,
    jobs,
    count
  };
}

export function receiveBookmarkedJobsActionCreator(bookmarkedJobs: BookmarkModel[],
                                                   count: number): ReceiveJobsAction {
  const jobs: JobModel[] = [];
  for (const bookmarkedJob of bookmarkedJobs) {
    jobs.push(bookmarkedJob.content_object as JobModel);
  }
  return {
    type: actionTypes.RECEIVE_JOBS,
    jobs,
    count
  };
}

export function bookmarkJobActionCreator(jobName: string) {
  return {
    type: actionTypes.BOOKMARK_JOB,
    jobName,
  };
}

export function unbookmarkJobActionCreator(jobName: string) {
  return {
    type: actionTypes.UNBOOKMARK_JOB,
    jobName,
  };
}

function _fetchJobs(jobsUrl: string,
                    bookmarks: boolean,
                    filters: { [key: string]: number | boolean | string } = {},
                    dispatch: any,
                    getState: any): any {
  dispatch(requestJobsActionCreator());
  const urlPieces = location.hash.split('?');
  const baseUrl = urlPieces[0];
  if (Object.keys(filters).length) {
    jobsUrl += url.format({query: filters});
    if (baseUrl) {
      history.push(baseUrl + url.format({query: filters}));
    }
  } else if (urlPieces.length > 1) {
    history.push(baseUrl);
  }
  return fetch(
    jobsUrl, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
    .then((response) => handleAuthError(response, dispatch))
    .then((response) => response.json())
    .then((json) => bookmarks ?
      dispatch(receiveBookmarkedJobsActionCreator(json.results, json.count)) :
      dispatch(receiveJobsActionCreator(json.results, json.count)));
}

export function fetchBookmarkedJobs(user: string,
                                    filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const jobsUrl = `${BASE_API_URL}/bookmarks/${user}/jobs/`;
    return _fetchJobs(jobsUrl, true, filters, dispatch, getState);
  };
}

export function fetchJobs(projectUniqueName: string,
                          filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const jobsUrl = `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/jobs`;
    return _fetchJobs(jobsUrl, false, filters, dispatch, getState);
  };
}

export function fetchJob(user: string, projectName: string, jobId: number): any {
  const jobUrl = getJobUrl(user, projectName, jobId, false);
  return (dispatch: any, getState: any) => {
    dispatch(requestJobActionCreator());
    return fetch(
      `${BASE_API_URL}${jobUrl}`, {
        headers: {
          Authorization: 'token ' + getState().auth.token
        }
      })
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.json())
      .then((json) => dispatch(receiveJobActionCreator(json)));
  };
}

export function bookmark(user: string, projectName: string, jobId: number | string): any {
  const jobName = getJobUniqueName(user, projectName, jobId);
  const jobUrl = getJobUrl(user, projectName, jobId, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${jobUrl}/bookmark`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(bookmarkJobActionCreator(jobName)));
  };
}

export function unbookmark(user: string, projectName: string, jobId: number | string): any {
  const jobName = getJobUniqueName(user, projectName, jobId);
  const jobUrl = getJobUrl(user, projectName, jobId, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${jobUrl}/unbookmark`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(unbookmarkJobActionCreator(jobName)));
  };
}
