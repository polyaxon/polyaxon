import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { getNotebookApiUrlFromName, getProjectUrl } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface ArchiveNotebookRequestAction extends Action {
  type: actionTypes.ARCHIVE_NOTEBOOK_REQUEST;
  notebookName: string;
}

export interface ArchiveNotebookSuccessAction extends Action {
  type: actionTypes.ARCHIVE_NOTEBOOK_SUCCESS;
  notebookName: string;
}

export interface ArchiveNotebookErrorAction extends Action {
  type: actionTypes.ARCHIVE_NOTEBOOK_ERROR;
  statusCode: number;
  error: any;
  notebookName: string;
}

export function archiveNotebookRequestActionCreator(notebookName: string): ArchiveNotebookRequestAction {
  return {
    type: actionTypes.ARCHIVE_NOTEBOOK_REQUEST,
    notebookName
  };
}

export function archiveNotebookSuccessActionCreator(notebookName: string): ArchiveNotebookSuccessAction {
  return {
    type: actionTypes.ARCHIVE_NOTEBOOK_SUCCESS,
    notebookName
  };
}

export function archiveNotebookErrorActionCreator(statusCode: number,
                                                  error: any,
                                                  notebookName: string): ArchiveNotebookErrorAction {
  return {
    type: actionTypes.ARCHIVE_NOTEBOOK_ERROR,
    statusCode,
    error,
    notebookName
  };
}

export type ArchiveNotebookAction =
  ArchiveNotebookRequestAction
  | ArchiveNotebookSuccessAction
  | ArchiveNotebookErrorAction;

export function archiveNotebook(notebookName: string, redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const notebookUrl = getNotebookApiUrlFromName(notebookName, false);

    dispatch(archiveNotebookRequestActionCreator(notebookName));

    return fetch(
      `${BASE_API_URL}${notebookUrl}/archive`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        archiveNotebookErrorActionCreator,
        'Notebook not found',
        'Failed to archive notebook',
        [notebookName]))
      .then(() => {
        const dispatched = dispatch(archiveNotebookSuccessActionCreator(notebookName));
        if (redirect) {
          const values = notebookName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#notebooks');
        }
        return dispatched;
      });
  };
}
