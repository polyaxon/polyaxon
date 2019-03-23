import { Action } from 'redux';
import * as url from 'url';

import { BASE_API_URL } from '../../constants/api';
import { urlifyProjectName } from '../../constants/utils';
import history from '../../history';
import { BookmarkModel } from '../../models/bookmark';
import { JobModel } from '../../models/job';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface FetchJobsRequestAction extends Action {
  type: actionTypes.FETCH_JOBS_REQUEST;
}

export interface FetchJobsSuccessAction extends Action {
  type: actionTypes.FETCH_JOBS_SUCCESS;
  jobs: JobModel[];
  count: number;
}

export interface FetchJobsErrorAction extends Action {
  type: actionTypes.FETCH_JOBS_ERROR;
  statusCode: number;
  error: any;
}

export function fetchJobsRequestActionCreator(): FetchJobsRequestAction {
  return {
    type: actionTypes.FETCH_JOBS_REQUEST,
  };
}

export function fetchJobsSuccessActionCreator(jobs: JobModel[], count: number): FetchJobsSuccessAction {
  return {
    type: actionTypes.FETCH_JOBS_SUCCESS,
    jobs,
    count
  };
}

export function fetchJobsErrorActionCreator(statusCode: number, error: any,): FetchJobsErrorAction {
  return {
    type: actionTypes.FETCH_JOBS_ERROR,
    statusCode,
    error,
  };
}

export function fetchBookmarkedJobsSuccessActionCreator(bookmarkedJobs: BookmarkModel[],
                                                        count: number): FetchJobsSuccessAction {
  const jobs: JobModel[] = [];
  for (const bookmarkedJob of bookmarkedJobs) {
    jobs.push(bookmarkedJob.content_object as JobModel);
  }
  return {
    type: actionTypes.FETCH_JOBS_SUCCESS,
    jobs,
    count
  };
}

export type FetchJobAction =
  FetchJobsRequestAction
  | FetchJobsSuccessAction
  | FetchJobsErrorAction;

function _fetchJobs(jobsUrl: string,
                    endpointList: string,
                    filters: { [key: string]: number | boolean | string } = {},
                    dispatch: any,
                    getState: any): any {

  dispatch(fetchJobsRequestActionCreator());

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
      dispatch(fetchBookmarkedJobsSuccessActionCreator(results, count));
    } else {
      dispatch(fetchJobsSuccessActionCreator(results, count));
    }
  };

  return fetch(
    jobsUrl, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
    .then((response) => stdHandleError(
      response,
      dispatch,
      fetchJobsErrorActionCreator,
      'Jobs not found',
      'Failed to fetch jobs'))
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
