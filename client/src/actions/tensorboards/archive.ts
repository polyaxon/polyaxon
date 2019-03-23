import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getProjectUrl, getTensorboardApiUrlFromName } from '../../constants/utils';
import history from '../../history';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface ArchiveTensorboardRequestAction extends Action {
  type: actionTypes.ARCHIVE_TENSORBOARD_REQUEST;
  tensorboardName: string;
}

export interface ArchiveTensorboardSuccessAction extends Action {
  type: actionTypes.ARCHIVE_TENSORBOARD_SUCCESS;
  tensorboardName: string;
}

export interface ArchiveTensorboardErrorAction extends Action {
  type: actionTypes.ARCHIVE_TENSORBOARD_ERROR;
  statusCode: number;
  error: any;
  tensorboardName: string;
}

export function archiveTensorboardRequestActionCreator(tensorboardName: string): ArchiveTensorboardRequestAction {
  return {
    type: actionTypes.ARCHIVE_TENSORBOARD_REQUEST,
    tensorboardName
  };
}

export function archiveTensorboardSuccessActionCreator(tensorboardName: string): ArchiveTensorboardSuccessAction {
  return {
    type: actionTypes.ARCHIVE_TENSORBOARD_SUCCESS,
    tensorboardName
  };
}

export function archiveTensorboardErrorActionCreator(statusCode: number,
                                                     error: any,
                                                     tensorboardName: string): ArchiveTensorboardErrorAction {
  return {
    type: actionTypes.ARCHIVE_TENSORBOARD_ERROR,
    statusCode,
    error,
    tensorboardName
  };
}

export type ArchiveTensorboardAction =
  ArchiveTensorboardRequestAction
  | ArchiveTensorboardSuccessAction
  | ArchiveTensorboardErrorAction;

export function archiveTensorboard(tensorboardName: string, redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const tensorboardUrl = getTensorboardApiUrlFromName(tensorboardName, false);

    dispatch(archiveTensorboardRequestActionCreator(tensorboardName));

    return fetch(
      `${BASE_API_URL}${tensorboardUrl}/archive`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        archiveTensorboardErrorActionCreator,
        'Tensorboard not found',
        'Failed to archive tensorboard',
        [tensorboardName]),
      )
      .then(() => {
        const dispatched = dispatch(archiveTensorboardSuccessActionCreator(tensorboardName));
        if (redirect) {
          const values = tensorboardName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#tensorboards');
        }
        return dispatched;
      });
  };
}
