import { Action } from 'redux';
import * as url from 'url';

import { BASE_API_URL } from '../constants/api';
import {
  getJobUrl,
  getProjectUrl,
  handleAuthError,
  urlifyProjectName
} from '../constants/utils';
import { getJobUrlFromName } from '../constants/utils';
import history from '../history';
import { BookmarkModel } from '../models/bookmark';
import { JobModel } from '../models/job';
import { ARCHIVES, BOOKMARKS } from '../utils/endpointList';

export enum actionTypes {
  CREATE_JOB = 'CREATE_JOB',
  DELETE_JOB = 'DELETE_JOB',
  STOP_JOB = 'STOP_JOB',
  ARCHIVE_JOB = 'ARCHIVE_JOB',
  RESTORE_JOB = 'RESTORE_JOB',
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
  jobName: string;
}

export interface ArchiveJobAction extends Action {
  type: actionTypes.ARCHIVE_JOB;
  jobName: string;
}

export interface RestoreJobAction extends Action {
  type: actionTypes.RESTORE_JOB;
  jobName: string;
}

export interface StopJobAction extends Action {
  type: actionTypes.STOP_JOB;
  jobName: string;
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
  | StopJobAction
  | ArchiveJobAction
  | RestoreJobAction
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

export function deleteJobActionCreator(jobName: string): DeleteJobAction {
  return {
    type: actionTypes.DELETE_JOB,
    jobName
  };
}

export function stopJobActionCreator(jobName: string): StopJobAction {
  return {
    type: actionTypes.STOP_JOB,
    jobName
  };
}

export function archiveJobActionCreator(jobName: string): ArchiveJobAction {
  return {
    type: actionTypes.ARCHIVE_JOB,
    jobName
  };
}

export function restoreJobActionCreator(jobName: string): RestoreJobAction {
  return {
    type: actionTypes.RESTORE_JOB,
    jobName
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
                    endpointList: string,
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

  const dispatchActionCreator = (results: any, count: number) => {
    if (endpointList === BOOKMARKS) {
      dispatch(receiveBookmarkedJobsActionCreator(results, count));
    } else {
      dispatch(receiveJobsActionCreator(results, count));
    }
  };

  return fetch(
    jobsUrl, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
    .then((response) => handleAuthError(response, dispatch))
    .then((response) => response.json())
    .then((json) => dispatchActionCreator(json.results, json.count));
}

export function fetchBookmarkedJobs(user: string,
                                    filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const jobsUrl = `${BASE_API_URL}/bookmarks/${user}/jobs/`;
    return _fetchJobs(jobsUrl, BOOKMARKS, filters, dispatch, getState);
  };
}

export function fetchArchivedJobs(user: string,
                                    filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const jobsUrl = `${BASE_API_URL}/archives/${user}/jobs/`;
    return _fetchJobs(jobsUrl, ARCHIVES, filters, dispatch, getState);
  };
}

export function fetchJobs(projectUniqueName: string,
                          filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const jobsUrl = `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/jobs`;
    return _fetchJobs(jobsUrl, '', filters, dispatch, getState);
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

export function updateJob(jobName: string, updateDict: { [key: string]: any }): any {
  const jobUrl = getJobUrlFromName(jobName, false);
  return (dispatch: any, getState: any) => {
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
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.json())
      .then((json) => dispatch(updateJobActionCreator(json)));
  };
}

export function deleteJob(jobName: string, redirect: boolean = false): any {
  const jobUrl = getJobUrlFromName(jobName, false);
  return (dispatch: any, getState: any) => {
    fetch(
      `${BASE_API_URL}${jobUrl}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => {
        const dispatched = dispatch(deleteJobActionCreator(jobName));
        if (redirect) {
          const values = jobName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#jobs');
        }
        return dispatched;
      });
  };
}

export function stopJob(jobName: string): any {
  const jobUrl = getJobUrlFromName(jobName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${jobUrl}/stop`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(stopJobActionCreator(jobName)));
  };
}

export function archiveJob(jobName: string, redirect: boolean = false): any {
  const jobUrl = getJobUrlFromName(jobName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${jobUrl}/archive`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => {
        const dispatched = dispatch(archiveJobActionCreator(jobName));
        if (redirect) {
          const values = jobName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#jobs');
        }
        return dispatched;
      });
  };
}

export function restoreJob(jobName: string): any {
  const jobUrl = getJobUrlFromName(jobName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${jobUrl}/restore`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(restoreJobActionCreator(jobName)));
  };
}

export function bookmark(jobName: string): any {
  const jobUrl = getJobUrlFromName(jobName, false);
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

export function unbookmark(jobName: string): any {
  const jobUrl = getJobUrlFromName(jobName, false);
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
