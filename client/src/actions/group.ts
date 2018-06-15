import { Action } from 'redux';
import * as url from 'url';

import { handleAuthError, urlifyProjectName } from '../constants/utils';
import { GroupModel } from '../models/group';
import { BASE_API_URL } from '../constants/api';
import * as paginationActions from '../actions/pagination';
import { getOffset } from '../constants/paginate';

export enum actionTypes {
  CREATE_GROUP = 'CREATE_GROUP',
  DELETE_GROUP = 'DELETE_GROUP',
  UPDATE_GROUP = 'UPDATE_GROUP',
  RECEIVE_GROUP = 'RECEIVE_GROUP',
  RECEIVE_GROUPS = 'RECEIVE_GROUPS',
  REQUEST_GROUP = 'REQUEST_GROUP',
  REQUEST_GROUPS = 'REQUEST_GROUPS',
}

export interface CreateUpdateReceiveGroupAction extends Action {
  type: actionTypes.CREATE_GROUP | actionTypes.UPDATE_GROUP | actionTypes.RECEIVE_GROUP;
  group: GroupModel;
}

export interface DeleteGroupAction extends Action {
  type: actionTypes.DELETE_GROUP;
  group: GroupModel;
}

export interface ReceiveGroupsAction extends Action {
  type: actionTypes.RECEIVE_GROUPS;
  groups: GroupModel[];
}

export interface RequestGroupsAction extends Action {
  type: actionTypes.REQUEST_GROUPS;
}

export type GroupAction =
  CreateUpdateReceiveGroupAction
  | DeleteGroupAction
  | ReceiveGroupsAction
  | RequestGroupsAction;

export function createGroupActionCreator(group: GroupModel): CreateUpdateReceiveGroupAction {
  return {
    type: actionTypes.CREATE_GROUP,
    group
  };
}

export function updateGroupActionCreator(group: GroupModel): CreateUpdateReceiveGroupAction {
  return {
    type: actionTypes.UPDATE_GROUP,
    group
  };
}

export function deleteGroupActionCreator(group: GroupModel): DeleteGroupAction {
  return {
    type: actionTypes.DELETE_GROUP,
    group
  };
}

export function requestGroupsActionCreator(): RequestGroupsAction {
  return {
    type: actionTypes.REQUEST_GROUPS,
  };
}

export function receiveGroupsActionCreator(groups: GroupModel[]): ReceiveGroupsAction {
  return {
    type: actionTypes.RECEIVE_GROUPS,
    groups
  };
}

export function receiveGroupActionCreator(group: GroupModel): CreateUpdateReceiveGroupAction {
  return {
    type: actionTypes.RECEIVE_GROUP,
    group
  };
}

export function fetchGroups(projectUniqueName: string, currentPage?: number): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestGroupsActionCreator());
    paginationActions.paginateGroup(dispatch, currentPage);
    let groupsUrl = BASE_API_URL + `/${urlifyProjectName(projectUniqueName)}` + '/groups/';
    let offset = getOffset(currentPage);
    if (offset != null) {
      groupsUrl += url.format({query: {offset: offset}});
    }
    return fetch(groupsUrl, {
      headers: {
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then(response => handleAuthError(response, dispatch))
      .then(response => response.json())
      .then(json => json.results)
      .then(json => dispatch(receiveGroupsActionCreator(json)));
  };
}

export function fetchGroup(user: string, projectName: string, groupId: number): any {
  return (dispatch: any, getState: any) => {
    dispatch(requestGroupsActionCreator());
    return fetch(BASE_API_URL + `/${user}` + `/${projectName}` + `/groups/` + `${groupId}`, {
      headers: {
        'Authorization': 'token ' + getState().auth.token
      }
    })
      .then(response => handleAuthError(response, dispatch))
      .then(response => response.json())
      .then(json => dispatch(receiveGroupActionCreator(json)));
  };
}
