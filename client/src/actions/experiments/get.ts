import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { ExperimentModel } from '../../models/experiment';
import { getExperimentUniqueName, getExperimentUrl, getExperimentUrlFromName } from '../../urls/utils';
import { getCodeReference } from '../codeReference';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface GetExperimentRequestAction extends Action {
  type: actionTypes.GET_EXPERIMENT_REQUEST;
  experimentName: string;
}

export interface GetExperimentSuccessAction extends Action {
  type: actionTypes.GET_EXPERIMENT_SUCCESS;
  experiment: ExperimentModel;
  experimentName: string;
}

export interface GetExperimentErrorAction extends Action {
  type: actionTypes.GET_EXPERIMENT_ERROR;
  statusCode: number;
  error: any;
  experimentName: string;
}

export function getExperimentRequestActionCreator(experimentName: string): GetExperimentRequestAction {
  return {
    type: actionTypes.GET_EXPERIMENT_REQUEST,
    experimentName
  };
}

export function getExperimentSuccessActionCreator(experiment: ExperimentModel): GetExperimentSuccessAction {
  return {
    type: actionTypes.GET_EXPERIMENT_SUCCESS,
    experiment,
    experimentName: experiment.unique_name
  };
}

export function getExperimentErrorActionCreator(statusCode: number,
                                                error: any,
                                                experimentName: string): GetExperimentErrorAction {
  return {
    type: actionTypes.GET_EXPERIMENT_ERROR,
    statusCode,
    error,
    experimentName
  };
}

export type GetExperimentAction =
  GetExperimentRequestAction
  | GetExperimentSuccessAction
  | GetExperimentErrorAction;

export function getExperimentCodeReference(experimentName: string): any {
  const experimentUrl = getExperimentUrlFromName(experimentName, false);
  const codeRefUrl = `${experimentUrl}/coderef`;
  return getCodeReference(codeRefUrl);
}

export function getExperiment(user: string, projectName: string, experimentId: number): any {
  return (dispatch: any, getState: any) => {
    const experimentUrl = getExperimentUrl(user, projectName, experimentId, false);
    const experimentName = getExperimentUniqueName(user, projectName, experimentId);

    dispatch(getExperimentRequestActionCreator(experimentName));

    return fetch(`${BASE_API_URL}${experimentUrl}`, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        getExperimentErrorActionCreator,
        'Experiment not found',
        'Failed to fetch experiment',
        [experimentName]))
      .then((response) => response.json())
      .then((json) => dispatch(getExperimentSuccessActionCreator(json)));
  };
}
