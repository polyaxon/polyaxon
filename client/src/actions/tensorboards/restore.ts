import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getTensorboardApiUrlFromName } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface RestoreTensorboardRequestAction extends Action {
  type: actionTypes.RESTORE_TENSORBOARD_REQUEST;
  tensorboardName: string;
}

export interface RestoreTensorboardSuccessAction extends Action {
  type: actionTypes.RESTORE_TENSORBOARD_SUCCESS;
  tensorboardName: string;
}

export interface RestoreTensorboardErrorAction extends Action {
  type: actionTypes.RESTORE_TENSORBOARD_ERROR;
  statusCode: number;
  error: any;
  tensorboardName: string;
}

export function restoreTensorboardRequestActionCreator(tensorboardName: string): RestoreTensorboardRequestAction {
  return {
    type: actionTypes.RESTORE_TENSORBOARD_REQUEST,
    tensorboardName
  };
}

export function restoreTensorboardSuccessActionCreator(tensorboardName: string): RestoreTensorboardSuccessAction {
  return {
    type: actionTypes.RESTORE_TENSORBOARD_SUCCESS,
    tensorboardName
  };
}

export function restoreTensorboardErrorActionCreator(statusCode: number,
                                                     error: any,
                                                     tensorboardName: string): RestoreTensorboardErrorAction {
  return {
    type: actionTypes.RESTORE_TENSORBOARD_ERROR,
    statusCode,
    error,
    tensorboardName
  };
}

export type RestoreTensorboardAction =
  RestoreTensorboardRequestAction
  | RestoreTensorboardSuccessAction
  | RestoreTensorboardErrorAction;

export function restoreTensorboard(tensorboardName: string): any {
  return (dispatch: any, getState: any) => {
    const tensorboardUrl = getTensorboardApiUrlFromName(tensorboardName, false);

    dispatch(restoreTensorboardRequestActionCreator(tensorboardName));

    return fetch(
      `${BASE_API_URL}${tensorboardUrl}/restore`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        restoreTensorboardErrorActionCreator,
        'Tensorboard not found',
        'Failed to restore tensorboard',
        [tensorboardName]))
      .then(() => dispatch(restoreTensorboardSuccessActionCreator(tensorboardName)));
  };
}
