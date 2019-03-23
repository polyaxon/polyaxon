import { Action } from 'redux';

import { BASE_API_URL } from '../../constants/api';
import { getGroupUrlFromName, getProjectUrlFromName } from '../../constants/utils';
import history from '../../history';
import { GroupModel } from '../../models/group';
import { stdCreateHandleError } from '../utils';
import { actionTypes } from './actionTypes';
import { getGroupSuccessActionCreator } from './get';

export interface CreateGroupRequestAction extends Action {
  type: actionTypes.CREATE_GROUP_REQUEST;
}

export interface CreateGroupErrorAction extends Action {
  type: actionTypes.CREATE_GROUP_ERROR;
  statusCode: number;
  error: any;
}

export function createGroupRequestActionCreator(): CreateGroupRequestAction {
  return {
    type: actionTypes.CREATE_GROUP_REQUEST,
  };
}

export function createGroupErrorActionCreator(statusCode: number, error: any): CreateGroupErrorAction {
  return {
    type: actionTypes.CREATE_GROUP_ERROR,
    statusCode,
    error
  };
}

export type CreateGroupAction =
  CreateGroupRequestAction
  | CreateGroupErrorAction;

export function createGroup(user: string,
                            projectName: string,
                            group: GroupModel,
                            redirect: boolean = false): any {
  return (dispatch: any, getState: any) => {

    dispatch(createGroupRequestActionCreator());

    return fetch(
      `${BASE_API_URL}/${user}/${projectName}/groups`, {
        method: 'POST',
        body: JSON.stringify(group),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => stdCreateHandleError(
        response,
        dispatch,
        createGroupErrorActionCreator,
        'Not found',
        'Failed to create group'))
      .then((response) => response.json())
      .then((json) => {
        const dispatched = dispatch(getGroupSuccessActionCreator(json));
        if (redirect) {
          history.push(getGroupUrlFromName( json.unique_name, true));
        }
        return dispatched;
      })
      .catch((response) => {
        if (response.status === 400) {
          return response.value.json().then(
            (value: any) => dispatch(createGroupErrorActionCreator(response.status, value)));
        } else {
          return response.value;
        }
      });
  };
}
