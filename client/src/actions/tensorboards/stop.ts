import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getTensorboardApiUrlFromName } from '../../constants/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';


export interface StopTensorboardRequestAction extends Action {
  type: actionTypes.STOP_TENSORBOARD_REQUEST;
  tensorboardName: string;
}

export interface StopTensorboardSuccessAction extends Action {
  type: actionTypes.STOP_TENSORBOARD_SUCCESS;
  tensorboardName: string;
}

export interface StopTensorboardErrorAction extends Action {
  type: actionTypes.STOP_TENSORBOARD_ERROR;
  statusCode: number;
  error: any;
  tensorboardName: string;
}

export function stopTensorboardRequestActionCreator(tensorboardName: string): StopTensorboardRequestAction {
  return {
    type: actionTypes.STOP_TENSORBOARD_REQUEST,
    tensorboardName
  };
}

export function stopTensorboardSuccessActionCreator(tensorboardName: string): StopTensorboardSuccessAction {
  return {
    type: actionTypes.STOP_TENSORBOARD_SUCCESS,
    tensorboardName
  };
}

export function stopTensorboardErrorActionCreator(statusCode: number,
                                                  error: any,
                                                  tensorboardName: string): StopTensorboardErrorAction {
  return {
    type: actionTypes.STOP_TENSORBOARD_ERROR,
    statusCode,
    error,
    tensorboardName
  };
}

export type StopTensorboardAction =
  StopTensorboardRequestAction
  | StopTensorboardSuccessAction
  | StopTensorboardErrorAction;

export function stopTensorboard(tensorboardName: string): any {
  return (dispatch: any, getState: any) => {
    const tensorboardUrl = getTensorboardApiUrlFromName(tensorboardName, false);

    dispatch(stopTensorboardRequestActionCreator(tensorboardName));

    return fetch(
      `${BASE_API_URL}${tensorboardUrl}/stop`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        stopTensorboardErrorActionCreator,
        'Tensorboard not found',
        'Failed to stop tensorboard',
        [tensorboardName]))
      .then(() => dispatch(stopTensorboardSuccessActionCreator(tensorboardName)));
  };
}

