import { Action } from 'redux';
import * as url from 'url';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { ExperimentJobModel } from '../../models/experimentJob';
import { urlifyProjectName } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface FetchExperimentJobsRequestAction extends Action {
  type: actionTypes.FETCH_EXPERIMENT_JOBS_REQUEST;
}

export interface FetchExperimentJobsSuccessAction extends Action {
  type: actionTypes.FETCH_EXPERIMENT_JOBS_SUCCESS;
  jobs: ExperimentJobModel[];
  count: number;
}

export interface FetchExperimentJobsErrorAction extends Action {
  type: actionTypes.FETCH_EXPERIMENT_JOBS_ERROR;
  statusCode: number;
  error: any;
}

export function fetchExperimentJobsRequestActionCreator(): FetchExperimentJobsRequestAction {
  return {
    type: actionTypes.FETCH_EXPERIMENT_JOBS_REQUEST,
  };
}

export function fetchExperimentJobsSuccessActionCreator(jobs: ExperimentJobModel[],
                                                        count: number): FetchExperimentJobsSuccessAction {
  return {
    type: actionTypes.FETCH_EXPERIMENT_JOBS_SUCCESS,
    jobs,
    count
  };
}

export function fetchExperimentJobsErrorActionCreator(statusCode: number,
                                                      error: any): FetchExperimentJobsErrorAction {
  return {
    type: actionTypes.FETCH_EXPERIMENT_JOBS_ERROR,
    statusCode,
    error
  };
}

export type FetchExperimentJobAction =
  FetchExperimentJobsRequestAction
  | FetchExperimentJobsSuccessAction
  | FetchExperimentJobsErrorAction;

export function fetchExperimentJobs(projectUniqueName: string,
                                    experimentId: number,
                                    filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    dispatch(fetchExperimentJobsRequestActionCreator());

    let jobsUrl =
      `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/experiments/${experimentId}/jobs`;
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
      .then((response) => stdHandleError(
        response,
        dispatch,
        fetchExperimentJobsErrorActionCreator,
        'Experiment jobs not found',
        'Failed to fetch experiment jobs'))
      .then((response) => response.json())
      .then((json) => dispatch(fetchExperimentJobsSuccessActionCreator(json.results, json.count)));
  };
}
