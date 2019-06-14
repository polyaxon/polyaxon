import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { TensorboardModel } from '../../models/tensorboard';
import { getTensorboardApiUrlFromName } from '../../urls/utils';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface UpdateTensorboardRequestAction extends Action {
  type: actionTypes.UPDATE_TENSORBOARD_REQUEST;
  tensorboardName: string;
}

export interface UpdateTensorboardSuccessAction extends Action {
  type: actionTypes.UPDATE_TENSORBOARD_SUCCESS;
  tensorboard: TensorboardModel;
  tensorboardName: string;
}

export interface UpdateTensorboardErrorAction extends Action {
  type: actionTypes.UPDATE_TENSORBOARD_ERROR;
  statusCode: number;
  error: any;
  tensorboardName: string;
}

export function updateTensorboardRequestActionCreator(tensorboardName: string): UpdateTensorboardRequestAction {
  return {
    type: actionTypes.UPDATE_TENSORBOARD_REQUEST,
    tensorboardName
  };
}

export function updateTensorboardSuccessActionCreator(tensorboard: TensorboardModel): UpdateTensorboardSuccessAction {
  return {
    type: actionTypes.UPDATE_TENSORBOARD_SUCCESS,
    tensorboard,
    tensorboardName: tensorboard.unique_name
  };
}

export function updateTensorboardErrorActionCreator(statusCode: number,
                                                    error: any,
                                                    tensorboardName: string): UpdateTensorboardErrorAction {
  return {
    type: actionTypes.UPDATE_TENSORBOARD_ERROR,
    statusCode,
    error,
    tensorboardName
  };
}

export type UpdateTensorboardAction =
  UpdateTensorboardRequestAction
  | UpdateTensorboardSuccessAction
  | UpdateTensorboardErrorAction;

export function updateTensorboard(tensorboardName: string, updateDict: { [key: string]: any }): any {
  return (dispatch: any, getState: any) => {
    const tensorboardUrl = getTensorboardApiUrlFromName(tensorboardName, false);

    dispatch(updateTensorboardRequestActionCreator(tensorboardName));

    return fetch(
      `${BASE_API_URL}${tensorboardUrl}`, {
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
        updateTensorboardErrorActionCreator,
        'Tensorboard not found',
        'Failed to tensorboard',
        [tensorboardName]))
      .then((response) => response.json())
      .then((json) => dispatch(updateTensorboardSuccessActionCreator(json)))
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(updateTensorboardErrorActionCreator(response.status, value, tensorboardName)));
        } else {
          return dispatch(updateTensorboardErrorActionCreator(response.status, response.value, tensorboardName));
        }
      });
  };
}
