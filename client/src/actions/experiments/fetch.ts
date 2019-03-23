import { Action } from 'redux';
import * as url from 'url';

import { BASE_API_URL } from '../../constants/api';
import { urlifyProjectName } from '../../constants/utils';
import history from '../../history';
import { BookmarkModel } from '../../models/bookmark';
import { ExperimentModel } from '../../models/experiment';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface FetchExperimentsRequestAction extends Action {
  type: actionTypes.FETCH_EXPERIMENTS_REQUEST;
}

export interface FetchExperimentsSuccessAction extends Action {
  type: actionTypes.FETCH_EXPERIMENTS_SUCCESS;
  experiments: ExperimentModel[];
  count: number;
}

export interface FetchExperimentsErrorAction extends Action {
  type: actionTypes.FETCH_EXPERIMENTS_ERROR;
  statusCode: number;
  error: any;
}

export interface FetchExperimentsParamsSuccessAction extends Action {
  type: actionTypes.FETCH_EXPERIMENTS_PARAMS_SUCCESS;
  experiments: ExperimentModel[];
  count: number;
}

export function fetchExperimentsRequestActionCreator(): FetchExperimentsRequestAction {
  return {
    type: actionTypes.FETCH_EXPERIMENTS_REQUEST,
  };
}

export function fetchExperimentsSuccessActionCreator(experiments: ExperimentModel[],
                                                     count: number): FetchExperimentsSuccessAction {
  return {
    type: actionTypes.FETCH_EXPERIMENTS_SUCCESS,
    experiments,
    count
  };
}

export function fetchExperimentsErrorActionCreator(statusCode: number, error: any): FetchExperimentsErrorAction {
  return {
    type: actionTypes.FETCH_EXPERIMENTS_ERROR,
    statusCode,
    error,
  };
}

export function fetchExperimentsParamsSuccessActionCreator(experiments: ExperimentModel[],
                                                           count: number): FetchExperimentsParamsSuccessAction {
  return {
    type: actionTypes.FETCH_EXPERIMENTS_PARAMS_SUCCESS,
    experiments,
    count
  };
}

export function fetchBookmarkedExperimentsSuccessActionCreator(bookmarkedExperiments: BookmarkModel[],
                                                               count: number): FetchExperimentsSuccessAction {
  const experiments: ExperimentModel[] = [];
  for (const bookmarkedExperiment of bookmarkedExperiments) {
    experiments.push(bookmarkedExperiment.content_object as ExperimentModel);
  }
  return {
    type: actionTypes.FETCH_EXPERIMENTS_SUCCESS,
    experiments,
    count
  };
}

export type FetchExperimentAction =
  FetchExperimentsRequestAction
  | FetchExperimentsSuccessAction
  | FetchExperimentsErrorAction
  | FetchExperimentsParamsSuccessAction;

function _fetchExperiments(experimentsUrl: string,
                           endpointList: string,
                           filters: { [key: string]: number | boolean | string } = {},
                           dispatch: any,
                           getState: any,
                           updateHistory: boolean = true): any {
  dispatch(fetchExperimentsRequestActionCreator());

  const urlPieces = location.hash.split('?');
  const baseUrl = urlPieces[0];
  if (Object.keys(filters).length) {
    experimentsUrl += url.format({query: filters});
    if (baseUrl && updateHistory) {
      history.push(baseUrl + url.format({query: filters}));
    }
  } else if (urlPieces.length > 1 && updateHistory) {
    history.push(baseUrl);
  }

  const dispatchActionCreator = (results: any, count: number) => {
    if (filters && filters.declarations) {
      return dispatch(fetchExperimentsParamsSuccessActionCreator(results, count));
    }
    if (endpointList === BOOKMARKS) {
      dispatch(fetchBookmarkedExperimentsSuccessActionCreator(results, count));
    } else {
      dispatch(fetchExperimentsSuccessActionCreator(results, count));
    }
  };

  return fetch(experimentsUrl, {
    headers: {
      Authorization: 'token ' + getState().auth.token
    }
  })
    .then((response) => stdHandleError(
        response,
        dispatch,
        fetchExperimentsErrorActionCreator,
        'Experiments not found',
        'Failed to fetch experiments'))
    .then((response) => response.json())
    .then((json) => dispatchActionCreator(json.results, json.count));
}

export function fetchBookmarkedExperiments(user: string,
                                           filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const experimentsUrl = `${BASE_API_URL}/bookmarks/${user}/experiments/`;
    return _fetchExperiments(experimentsUrl, BOOKMARKS, filters, dispatch, getState);
  };
}

export function fetchArchivedExperiments(user: string,
                                         filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const experimentsUrl = `${BASE_API_URL}/archives/${user}/experiments/`;
    return _fetchExperiments(experimentsUrl, ARCHIVES, filters, dispatch, getState);
  };
}

export function fetchExperiments(projectUniqueName: string,
                                 filters: { [key: string]: number | boolean | string } = {},
                                 updateHistory: boolean = true): any {
  return (dispatch: any, getState: any) => {
    const experimentsUrl = `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/experiments/`;
    return _fetchExperiments(experimentsUrl, '', filters, dispatch, getState, updateHistory);
  };
}


