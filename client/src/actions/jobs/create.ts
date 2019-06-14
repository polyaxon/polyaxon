import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { JobModel } from '../../models/job';
import { getJobUrlFromName } from '../../urls/utils';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';
import { getJobSuccessActionCreator } from './get';

export interface CreateJobRequestAction extends Action {
  type: actionTypes.CREATE_JOB_REQUEST;
}

export interface CreateJobSuccessAction extends Action {
  type: actionTypes.CREATE_JOB_SUCCESS;
}

export interface CreateJobErrorAction extends Action {
  type: actionTypes.CREATE_JOB_ERROR;
  statusCode: number;
  error: any;
}

export function createJobRequestActionCreator(): CreateJobRequestAction {
  return {
    type: actionTypes.CREATE_JOB_REQUEST,
  };
}

export function createJobSuccessActionCreator(): CreateJobSuccessAction {
  return {
    type: actionTypes.CREATE_JOB_SUCCESS,
  };
}


export function createJobErrorActionCreator(statusCode: number, error: any): CreateJobErrorAction {
  return {
    type: actionTypes.CREATE_JOB_ERROR,
    statusCode,
    error
  };
}

export type CreateJobAction =
  CreateJobRequestAction
  | CreateJobSuccessAction
  | CreateJobErrorAction;

export function createJob(user: string,
                          projectName: string,
                          job: JobModel,
                          redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {

    dispatch(createJobRequestActionCreator());

    return fetch(`${BASE_API_URL}/${user}/${projectName}/jobs`, {
      method: 'POST',
      body: JSON.stringify(job),
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
        createJobErrorActionCreator,
        'Not found',
        'Failed to create job'))
      .then((response) => response.json())
      .then((json) => {
        dispatch(createJobSuccessActionCreator());
        const dispatched = dispatch(getJobSuccessActionCreator(json));
        if (redirect) {
          history.push(getJobUrlFromName(json.unique_name, true));
        }
        return dispatched;
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(createJobErrorActionCreator(response.status, value)));
        } else {
          return dispatch(createJobErrorActionCreator(response.status, response.value));
        }
      });
  };
}
