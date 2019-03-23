import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getExperimentUrlFromName } from '../../constants/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface RestoreExperimentRequestAction extends Action {
  type: actionTypes.RESTORE_EXPERIMENT_REQUEST;
  experimentName: string;
}

export interface RestoreExperimentSuccessAction extends Action {
  type: actionTypes.RESTORE_EXPERIMENT_SUCCESS;
  experimentName: string;
}

export interface RestoreExperimentErrorAction extends Action {
  type: actionTypes.RESTORE_EXPERIMENT_ERROR;
  statusCode: number;
  error: any;
  experimentName: string;
}

export function restoreExperimentRequestActionCreator(experimentName: string): RestoreExperimentRequestAction {
  return {
    type: actionTypes.RESTORE_EXPERIMENT_REQUEST,
    experimentName,
  };
}

export function restoreExperimentSuccessActionCreator(experimentName: string): RestoreExperimentSuccessAction {
  return {
    type: actionTypes.RESTORE_EXPERIMENT_SUCCESS,
    experimentName,
  };
}

export function restoreExperimentErrorActionCreator(statusCode: number,
                                                    error: any,
                                                    experimentName: string): RestoreExperimentErrorAction {
  return {
    type: actionTypes.RESTORE_EXPERIMENT_ERROR,
    statusCode,
    error,
    experimentName,
  };
}

export type RestoreExperimentAction =
  RestoreExperimentRequestAction
  | RestoreExperimentSuccessAction
  | RestoreExperimentErrorAction;

export function restoreExperiment(experimentName: string): any {
  return (dispatch: any, getState: any) => {
    const experimentUrl = getExperimentUrlFromName(experimentName, false);

    dispatch(restoreExperimentRequestActionCreator(experimentName));

    return fetch(`${BASE_API_URL}${experimentUrl}/restore`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        restoreExperimentErrorActionCreator,
        'Experiment not found',
        'Failed to restore experiment',
        [experimentName]))
      .then(() => dispatch(restoreExperimentSuccessActionCreator(experimentName)));
  };
}
