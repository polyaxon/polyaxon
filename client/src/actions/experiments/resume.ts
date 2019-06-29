import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { getExperimentUrlFromName } from '../../urls/utils';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';
import { getExperimentSuccessActionCreator } from './get';

export interface ResumeExperimentRequestAction extends Action {
  type: actionTypes.RESUME_EXPERIMENT_REQUEST;
  experimentName: string;
}

export interface ResumeExperimentSuccessAction extends Action {
  type: actionTypes.RESUME_EXPERIMENT_SUCCESS;
  experimentName: string;
}

export interface ResumeExperimentErrorAction extends Action {
  type: actionTypes.RESUME_EXPERIMENT_ERROR;
  statusCode: number;
  error: any;
  experimentName: string;
}

export function resumeExperimentRequestActionCreator(experimentName: string): ResumeExperimentRequestAction {
  return {
    type: actionTypes.RESUME_EXPERIMENT_REQUEST,
    experimentName,
  };
}

export function resumeExperimentSuccessActionCreator(experimentName: string): ResumeExperimentSuccessAction {
  return {
    type: actionTypes.RESUME_EXPERIMENT_SUCCESS,
    experimentName,
  };
}

export function resumeExperimentErrorActionCreator(statusCode: number,
                                                   error: any,
                                                   experimentName: string): ResumeExperimentErrorAction {
  return {
    type: actionTypes.RESUME_EXPERIMENT_ERROR,
    statusCode,
    error,
    experimentName,
  };
}

export type ResumeExperimentAction =
  ResumeExperimentRequestAction
  | ResumeExperimentSuccessAction
  | ResumeExperimentErrorAction;

export function resumeExperiment(experimentName: string, redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const experimentUrl = getExperimentUrlFromName(experimentName, false);

    dispatch(resumeExperimentRequestActionCreator(experimentName));

    return fetch(`${BASE_API_URL}${experimentUrl}/resume`, {
      method: 'POST',
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
        resumeExperimentErrorActionCreator,
        'Not found',
        'Failed to resume experiment',
        [experimentName]))
      .then((response) => response.json())
      .then((json) => {
        resumeExperimentSuccessActionCreator(experimentName);
        const dispatched = dispatch(getExperimentSuccessActionCreator(json));
        if (redirect) {
          history.push(getExperimentUrlFromName(json.unique_name, true));
        }
        return dispatched;
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(resumeExperimentErrorActionCreator(response.status, value, experimentName)));
        } else {
          return response.value;
        }
      });
  };
}
