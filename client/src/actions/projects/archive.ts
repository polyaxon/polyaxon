import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getProjectUrlFromName, getUserUrl } from '../../constants/utils';
import history from '../../history';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface ArchiveProjectRequestAction extends Action {
  type: actionTypes.ARCHIVE_PROJECT_REQUEST;
  projectName: string;
}

export interface ArchiveProjectSuccessAction extends Action {
  type: actionTypes.ARCHIVE_PROJECT_SUCCESS;
  projectName: string;
}

export interface ArchiveProjectErrorAction extends Action {
  type: actionTypes.ARCHIVE_PROJECT_ERROR;
  statusCode: number;
  error: any;
  projectName: string;
}

export function archiveProjectRequestActionCreator(projectName: string): ArchiveProjectRequestAction {
  return {
    type: actionTypes.ARCHIVE_PROJECT_REQUEST,
    projectName
  };
}

export function archiveProjectSuccessActionCreator(projectName: string): ArchiveProjectSuccessAction {
  return {
    type: actionTypes.ARCHIVE_PROJECT_SUCCESS,
    projectName
  };
}

export function archiveProjectErrorActionCreator(statusCode: number,
                                                 error: any,
                                                 projectName: string): ArchiveProjectErrorAction {
  return {
    type: actionTypes.ARCHIVE_PROJECT_ERROR,
    statusCode,
    error,
    projectName
  };
}

export type ArchiveProjectAction =
  ArchiveProjectRequestAction
  | ArchiveProjectSuccessAction
  | ArchiveProjectErrorAction;

export function archiveProject(projectName: string, redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const projectUrl = getProjectUrlFromName(projectName, false);

    dispatch(archiveProjectRequestActionCreator(projectName));

    return fetch(`${BASE_API_URL}${projectUrl}/archive`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => stdHandleError(
        response,
        dispatch,
        archiveProjectErrorActionCreator,
        'Project not found',
        'Failed to archive project',
        [projectName]),
      )
      .then(() => {
        const dispatched = dispatch(archiveProjectSuccessActionCreator(projectName));
        if (redirect) {
          const values = projectName.split('.');
          history.push(getUserUrl(values[0], true));
        }
        return dispatched;
      });
  };
}
