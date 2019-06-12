import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { getJobUrlFromName, getProjectUrl } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface ArchiveJobRequestAction extends Action {
  type: actionTypes.ARCHIVE_JOB_REQUEST;
  jobName: string;
}

export interface ArchiveJobSuccessAction extends Action {
  type: actionTypes.ARCHIVE_JOB_SUCCESS;
  jobName: string;
}

export interface ArchiveJobErrorAction extends Action {
  type: actionTypes.ARCHIVE_JOB_ERROR;
  statusCode: number;
  error: any;
  jobName: string;
}

export function archiveJobRequestActionCreator(jobName: string): ArchiveJobRequestAction {
  return {
    type: actionTypes.ARCHIVE_JOB_REQUEST,
    jobName
  };
}

export function archiveJobSuccessActionCreator(jobName: string): ArchiveJobSuccessAction {
  return {
    type: actionTypes.ARCHIVE_JOB_SUCCESS,
    jobName
  };
}

export function archiveJobErrorActionCreator(statusCode: number,
                                             error: any,
                                             jobName: string): ArchiveJobErrorAction {
  return {
    type: actionTypes.ARCHIVE_JOB_ERROR,
    statusCode,
    error,
    jobName
  };
}

export type ArchiveJobAction =
  ArchiveJobRequestAction
  | ArchiveJobSuccessAction
  | ArchiveJobErrorAction;

export function archiveJob(jobName: string, redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const jobUrl = getJobUrlFromName(jobName, false);

    dispatch(archiveJobRequestActionCreator(jobName));

    return fetch(
      `${BASE_API_URL}${jobUrl}/archive`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        archiveJobErrorActionCreator,
        'Job not found',
        'Failed to archive job',
        [jobName]),
      )
      .then(() => {
        const dispatched = dispatch(archiveJobSuccessActionCreator(jobName));
        if (redirect) {
          const values = jobName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#jobs');
        }
        return dispatched;
      });
  };
}
