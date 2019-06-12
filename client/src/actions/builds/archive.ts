import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { getBuildUrlFromName, getProjectUrl } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface ArchiveBuildRequestAction extends Action {
  type: actionTypes.ARCHIVE_BUILD_REQUEST;
  buildName: string;
}

export interface ArchiveBuildSuccessAction extends Action {
  type: actionTypes.ARCHIVE_BUILD_SUCCESS;
  buildName: string;
}

export interface ArchiveBuildErrorAction extends Action {
  type: actionTypes.ARCHIVE_BUILD_ERROR;
  statusCode: number;
  error: any;
  buildName: string;
}

export function archiveBuildRequestActionCreator(buildName: string): ArchiveBuildRequestAction {
  return {
    type: actionTypes.ARCHIVE_BUILD_REQUEST,
    buildName
  };
}

export function archiveBuildSuccessActionCreator(buildName: string): ArchiveBuildSuccessAction {
  return {
    type: actionTypes.ARCHIVE_BUILD_SUCCESS,
    buildName
  };
}

export function archiveBuildErrorActionCreator(statusCode: number,
                                               error: any,
                                               buildName: string): ArchiveBuildErrorAction {
  return {
    type: actionTypes.ARCHIVE_BUILD_ERROR,
    statusCode,
    error,
    buildName
  };
}

export type ArchiveBuildAction =
  ArchiveBuildRequestAction
  | ArchiveBuildSuccessAction
  | ArchiveBuildErrorAction;

export function archiveBuild(buildName: string, redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const buildUrl = getBuildUrlFromName(buildName, false);

    dispatch(archiveBuildRequestActionCreator(buildName));

    return fetch(
      `${BASE_API_URL}${buildUrl}/archive`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        archiveBuildErrorActionCreator,
        'Build not found',
        'Failed to archive build',
        [buildName]))
      .then(() => {
        const dispatched = dispatch(archiveBuildSuccessActionCreator(buildName));
        if (redirect) {
          const values = buildName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#builds');
        }
        return dispatched;
      });
  };
}
