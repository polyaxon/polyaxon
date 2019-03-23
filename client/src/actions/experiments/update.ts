import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getExperimentUrlFromName } from '../../constants/utils';
import { ExperimentModel } from '../../models/experiment';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface UpdateExperimentRequestAction extends Action {
  type: actionTypes.UPDATE_EXPERIMENT_REQUEST;
  experimentName: string;
}

export interface UpdateExperimentSuccessAction extends Action {
  type: actionTypes.UPDATE_EXPERIMENT_SUCCESS;
  experiment: ExperimentModel;
}

export interface UpdateExperimentErrorAction extends Action {
  type: actionTypes.UPDATE_EXPERIMENT_ERROR;
  statusCode: number;
  error: any;
  experimentName: string;
}

export function updateExperimentRequestActionCreator(experimentName: string): UpdateExperimentRequestAction {
  return {
    type: actionTypes.UPDATE_EXPERIMENT_REQUEST,
    experimentName
  };
}

export function updateExperimentSuccessActionCreator(experiment: ExperimentModel): UpdateExperimentSuccessAction {
  return {
    type: actionTypes.UPDATE_EXPERIMENT_SUCCESS,
    experiment
  };
}

export function updateExperimentErrorActionCreator(statusCode: number,
                                                   error: any,
                                                   experimentName: string): UpdateExperimentErrorAction {
  return {
    type: actionTypes.UPDATE_EXPERIMENT_ERROR,
    statusCode,
    error,
    experimentName
  };
}

export type UpdateExperimentAction =
  UpdateExperimentRequestAction
  | UpdateExperimentSuccessAction
  | UpdateExperimentErrorAction;

export function updateExperiment(experimentName: string, updateDict: { [key: string]: any }): any {
  return (dispatch: any, getState: any) => {
    const experimentUrl = getExperimentUrlFromName(experimentName, false);

    dispatch(updateExperimentRequestActionCreator(experimentName));

    return fetch(`${BASE_API_URL}${experimentUrl}`, {
      method: 'PATCH',
      body: JSON.stringify(updateDict),
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdCreateHandleError(
        response,
        dispatch,
        updateExperimentErrorActionCreator,
        'Experiment not found',
        'Failed to experiment',
        [experimentName]))
      .then((response) => response.json())
      .then((json) => dispatch(updateExperimentSuccessActionCreator(json)))
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(updateExperimentErrorActionCreator(response.status, value, experimentName)));
        } else {
          return response.value;
        }
      });
  };
}
