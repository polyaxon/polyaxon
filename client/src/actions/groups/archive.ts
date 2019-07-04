import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { getGroupUrlFromName, getProjectUrl } from '../../urls/utils';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface ArchiveGroupRequestAction extends Action {
  type: actionTypes.ARCHIVE_GROUP_REQUEST;
  groupName: string;
}

export interface ArchiveGroupSuccessAction extends Action {
  type: actionTypes.ARCHIVE_GROUP_SUCCESS;
  groupName: string;
}

export interface ArchiveGroupErrorAction extends Action {
  type: actionTypes.ARCHIVE_GROUP_ERROR;
  statusCode: number;
  error: any;
  groupName: string;
}

export function archiveGroupActionRequestCreator(groupName: string): ArchiveGroupRequestAction {
  return {
    type: actionTypes.ARCHIVE_GROUP_REQUEST,
    groupName
  };
}

export function archiveGroupActionSuccessCreator(groupName: string): ArchiveGroupSuccessAction {
  return {
    type: actionTypes.ARCHIVE_GROUP_SUCCESS,
    groupName
  };
}

export function archiveGroupActionErrorCreator(statusCode: number,
                                               error: any,
                                               groupName: string): ArchiveGroupErrorAction {
  return {
    type: actionTypes.ARCHIVE_GROUP_ERROR,
    statusCode,
    error,
    groupName
  };
}

export type ArchiveGroupAction =
  ArchiveGroupRequestAction
  | ArchiveGroupSuccessAction
  | ArchiveGroupErrorAction;

export function archiveGroup(groupName: string, redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {
    const groupUrl = getGroupUrlFromName(groupName, false);

    dispatch(archiveGroupActionRequestCreator(groupName));

    return fetch(
      `${BASE_API_URL}${groupUrl}/archive`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdHandleError(
        response,
        dispatch,
        archiveGroupActionErrorCreator,
        'Group not found',
        'Failed to archive group',
        [groupName]))
      .then(() => {
        const dispatched = dispatch(archiveGroupActionSuccessCreator(groupName));
        if (redirect) {
          const values = groupName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#groups');
        }
        return dispatched;
      });
  };
}
