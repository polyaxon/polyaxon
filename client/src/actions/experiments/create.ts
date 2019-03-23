import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getExperimentUrlFromName } from '../../constants/utils';
import history from '../../history';
import { ExperimentModel } from '../../models/experiment';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';
import { getExperimentSuccessActionCreator } from './get';

export interface CreateExperimentRequestAction extends Action {
  type: actionTypes.CREATE_EXPERIMENT_REQUEST;
}

export interface CreateExperimentErrorAction extends Action {
  type: actionTypes.CREATE_EXPERIMENT_ERROR;
  statusCode: number;
  error: any;
}

export function createExperimentRequestActionCreator(): CreateExperimentRequestAction {
  return {
    type: actionTypes.CREATE_EXPERIMENT_REQUEST,
  };
}

export function createExperimentErrorActionCreator(statusCode: number, error: any): CreateExperimentErrorAction {
  return {
    type: actionTypes.CREATE_EXPERIMENT_ERROR,
    statusCode,
    error
  };
}

export type CreateExperimentAction =
  CreateExperimentRequestAction
  | CreateExperimentErrorAction;

export function createExperiment(user: string,
                                 projectName: string,
                                 experiment: ExperimentModel,
                                 redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {

    dispatch(createExperimentRequestActionCreator());

    return fetch(`${BASE_API_URL}/${user}/${projectName}/experiments`, {
      method: 'POST',
      body: JSON.stringify(experiment),
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdCreateHandleError(
        response,
        dispatch,
        createExperimentErrorActionCreator,
        'Not found',
        'Failed to create experiment'))
      .then((response) => response.json())
      .then((json) => {
        const dispatched = dispatch(getExperimentSuccessActionCreator(json));
        if (redirect) {
          history.push(getExperimentUrlFromName( json.unique_name, true));
        }
        return dispatched;
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(createExperimentErrorActionCreator(response.status, value)));
        } else {
          return response.value;
        }
      });
  };
}
