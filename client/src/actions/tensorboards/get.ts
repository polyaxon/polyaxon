import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getTensorboardApiUrl, getTensorboardUniqueName } from '../../constants/utils';
import { TensorboardModel } from '../../models/tensorboard';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface GetTensorboardRequestAction extends Action {
  type: actionTypes.GET_TENSORBOARD_REQUEST;
  tensorboardName: string;
}

export interface GetTensorboardSuccessAction extends Action {
  type: actionTypes.GET_TENSORBOARD_SUCCESS;
  tensorboard: TensorboardModel;
  tensorboardName: string;
}

export interface GetTensorboardErrorAction extends Action {
  type: actionTypes.GET_TENSORBOARD_ERROR;
  statusCode: number;
  error: any;
  tensorboardName: string;
}

export function getTensorboardRequestActionCreator(tensorboardName: string): GetTensorboardRequestAction {
  return {
    type: actionTypes.GET_TENSORBOARD_REQUEST,
    tensorboardName,
  };
}

export function getTensorboardSuccessActionCreator(tensorboard: TensorboardModel): GetTensorboardSuccessAction {
  return {
    type: actionTypes.GET_TENSORBOARD_SUCCESS,
    tensorboard,
    tensorboardName: tensorboard.unique_name,
  };
}

export function getTensorboardErrorActionCreator(statusCode: number,
                                                 error: any,
                                                 tensorboardName: string): GetTensorboardErrorAction {
  return {
    type: actionTypes.GET_TENSORBOARD_ERROR,
    statusCode,
    error,
    tensorboardName,
  };
}

export type GetTensorboardAction =
  GetTensorboardRequestAction
  | GetTensorboardSuccessAction
  | GetTensorboardErrorAction;

export function fetchTensorboard(user: string, projectName: string, tensorboardId: number | string): any {
  return (dispatch: any, getState: any) => {
    const tensorboardUrl = getTensorboardApiUrl(user, projectName, tensorboardId, false);
    const tensorboardName = getTensorboardUniqueName(user, projectName, tensorboardId);

    dispatch(getTensorboardRequestActionCreator(tensorboardName));

    return fetch(
      `${BASE_API_URL}${tensorboardUrl}`, {
        headers: {
          Authorization: 'token ' + getState().auth.token
        }
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        getTensorboardErrorActionCreator,
        'Tensorboard not found',
        'Failed to fetch tensorboard',
        [tensorboardName]))
      .then((response) => response.json())
      .then((json) => dispatch(getTensorboardSuccessActionCreator(json)));
  };
}
