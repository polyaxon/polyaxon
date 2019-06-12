import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { getProjectUrl, getTensorboardApiUrlFromName } from '../../urls/utils';
import { stdDeleteHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface DeleteTensorboardRequestAction extends Action {
  type: actionTypes.DELETE_TENSORBOARD_REQUEST;
  tensorboardName: string;
}

export interface DeleteTensorboardSuccessAction extends Action {
  type: actionTypes.DELETE_TENSORBOARD_SUCCESS;
  tensorboardName: string;
}

export interface DeleteTensorboardErrorAction extends Action {
  type: actionTypes.DELETE_TENSORBOARD_ERROR;
  statusCode: number;
  error: any;
  tensorboardName: string;
}

export function deleteTensorboardRequestActionCreator(tensorboardName: string): DeleteTensorboardRequestAction {
  return {
    type: actionTypes.DELETE_TENSORBOARD_REQUEST,
    tensorboardName
  };
}

export function deleteTensorboardSuccessActionCreator(tensorboardName: string): DeleteTensorboardSuccessAction {
  return {
    type: actionTypes.DELETE_TENSORBOARD_SUCCESS,
    tensorboardName
  };
}

export function deleteTensorboardErrorActionCreator(statusCode: number,
                                                    error: any,
                                                    tensorboardName: string): DeleteTensorboardErrorAction {
  return {
    type: actionTypes.DELETE_TENSORBOARD_ERROR,
    statusCode,
    error,
    tensorboardName
  };
}

export type DeleteTensorboardAction =
  DeleteTensorboardRequestAction
  | DeleteTensorboardSuccessAction
  | DeleteTensorboardErrorAction;

export function deleteTensorboard(tensorboardName: string, redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const tensorboardUrl = getTensorboardApiUrlFromName(tensorboardName, false);

    dispatch(deleteTensorboardRequestActionCreator(tensorboardName));

    return fetch(
      `${BASE_API_URL}${tensorboardUrl}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdDeleteHandleError(
        response,
        dispatch,
        deleteTensorboardErrorActionCreator,
        'Tensorboard not found',
        'Failed to delete tensorboard',
        [tensorboardName]))
      .then(() => {
        const dispatched = dispatch(deleteTensorboardSuccessActionCreator(tensorboardName));
        if (redirect) {
          const values = tensorboardName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#tensorboards');
        }
        return dispatched;
      });
  };
}
