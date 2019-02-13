import { Action } from 'redux';
import * as url from 'url';

import { BASE_API_URL } from '../constants/api';
import {
  getGroupUrl,
  getGroupUrlFromName,
  getProjectNameFromUniqueName,
  getProjectUrl,
  getProjectUrlFromName,
  getSelectionUrlFromName,
  handleAuthError,
  urlifyProjectName
} from '../constants/utils';
import history from '../history';
import { BookmarkModel } from '../models/bookmark';
import { GroupModel } from '../models/group';
import { ARCHIVES, BOOKMARKS } from '../utils/endpointList';
import { deleteExperimentsActionCreator } from './experiment';

export enum actionTypes {
  CREATE_GROUP = 'CREATE_GROUP',
  DELETE_GROUP = 'DELETE_GROUP',
  STOP_GROUP = 'STOP_GROUP',
  ARCHIVE_GROUP = 'ARCHIVE_GROUP',
  RESTORE_GROUP = 'RESTORE_GROUP',
  UPDATE_GROUP = 'UPDATE_GROUP',
  RECEIVE_GROUP = 'RECEIVE_GROUP',
  RECEIVE_GROUPS = 'RECEIVE_GROUPS',
  REQUEST_GROUP = 'REQUEST_GROUP',
  REQUEST_GROUPS = 'REQUEST_GROUPS',
  BOOKMARK_GROUP = 'BOOKMARK_GROUP',
  UNBOOKMARK_GROUP = 'UNBOOKMARK_GROUP',
  START_GROUP_TENSORBOARD = 'START_GROUP_TENSORBOARD',
  STOP_GROUP_TENSORBOARD = 'STOP_GROUP_TENSORBOARD',
}

export interface CreateUpdateReceiveGroupAction extends Action {
  type: actionTypes.CREATE_GROUP | actionTypes.UPDATE_GROUP | actionTypes.RECEIVE_GROUP;
  group: GroupModel;
}

export interface DeleteGroupAction extends Action {
  type: actionTypes.DELETE_GROUP;
  groupName: string;
}

export interface StopGroupAction extends Action {
  type: actionTypes.STOP_GROUP;
  groupName: string;
}

export interface ArchiveGroupAction extends Action {
  type: actionTypes.ARCHIVE_GROUP;
  groupName: string;
}

export interface RestoreGroupAction extends Action {
  type: actionTypes.RESTORE_GROUP;
  groupName: string;
}

export interface ReceiveGroupsAction extends Action {
  type: actionTypes.RECEIVE_GROUPS;
  groups: GroupModel[];
  count: number;
}

export interface RequestGroupsAction extends Action {
  type: actionTypes.REQUEST_GROUPS;
}

export interface BookmarkGroupAction extends Action {
  type: actionTypes.BOOKMARK_GROUP | actionTypes.UNBOOKMARK_GROUP;
  groupName: string;
}

export interface GroupTensorboardAction extends Action {
  type: actionTypes.START_GROUP_TENSORBOARD | actionTypes.STOP_GROUP_TENSORBOARD;
  groupName: string;
}

export type GroupAction =
  CreateUpdateReceiveGroupAction
  | DeleteGroupAction
  | StopGroupAction
  | ArchiveGroupAction
  | RestoreGroupAction
  | ReceiveGroupsAction
  | RequestGroupsAction
  | BookmarkGroupAction
  | GroupTensorboardAction;

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

export function deleteGroupActionCreator(groupName: string): DeleteGroupAction {
  return {
    type: actionTypes.DELETE_GROUP,
    groupName
  };
}

export function stopGroupActionCreator(groupName: string): StopGroupAction {
  return {
    type: actionTypes.STOP_GROUP,
    groupName
  };
}

export function archiveGroupActionCreator(groupName: string): ArchiveGroupAction {
  return {
    type: actionTypes.ARCHIVE_GROUP,
    groupName
  };
}

export function restoreGroupActionCreator(groupName: string): RestoreGroupAction {
  return {
    type: actionTypes.RESTORE_GROUP,
    groupName
  };
}

export function requestGroupsActionCreator(): RequestGroupsAction {
  return {
    type: actionTypes.REQUEST_GROUPS,
  };
}

export function receiveGroupsActionCreator(groups: GroupModel[], count: number): ReceiveGroupsAction {
  return {
    type: actionTypes.RECEIVE_GROUPS,
    groups,
    count
  };
}

export function receiveBookmarkedGroupsActionCreator(bookmarkedGroups: BookmarkModel[],
                                                     count: number): ReceiveGroupsAction {
  const groups: GroupModel[] = [];
  for (const bookmarkedGroup of bookmarkedGroups) {
    groups.push(bookmarkedGroup.content_object as GroupModel);
  }
  return {
    type: actionTypes.RECEIVE_GROUPS,
    groups,
    count
  };
}

export function receiveGroupActionCreator(group: GroupModel): CreateUpdateReceiveGroupAction {
  return {
    type: actionTypes.RECEIVE_GROUP,
    group
  };
}

export function bookmarkGroupActionCreator(groupName: string) {
  return {
    type: actionTypes.BOOKMARK_GROUP,
    groupName,
  };
}

export function unbookmarkGroupActionCreator(groupName: string) {
  return {
    type: actionTypes.UNBOOKMARK_GROUP,
    groupName,
  };
}

export function startGroupTensorboardActionCreator(groupName: string) {
  return {
    type: actionTypes.START_GROUP_TENSORBOARD,
    groupName,
  };
}

export function stopGroupTensorboardActionCreator(groupName: string) {
  return {
    type: actionTypes.STOP_GROUP_TENSORBOARD,
    groupName,
  };
}

function _fetchGroups(groupsUrl: string,
                      endpointList: string,
                      filters: { [key: string]: number | boolean | string } = {},
                      dispatch: any,
                      getState: any): any {
  dispatch(requestGroupsActionCreator());
  const urlPieces = location.hash.split('?');
  const baseUrl = urlPieces[0];
  if (Object.keys(filters).length) {
    groupsUrl += url.format({query: filters});
    if (baseUrl) {
      history.push(baseUrl + url.format({query: filters}));
    }
  } else if (urlPieces.length > 1) {
    history.push(baseUrl);
  }

  const dispatchActionCreator = (results: any, count: number) => {
    if (endpointList === BOOKMARKS) {
      dispatch(receiveBookmarkedGroupsActionCreator(results, count));
    } else {
      dispatch(receiveGroupsActionCreator(results, count));
    }
  };

  return fetch(groupsUrl, {
    headers: {
      Authorization: 'token ' + getState().auth.token
    }
  })
    .then((response) => handleAuthError(response, dispatch))
    .then((response) => response.json())
    .then((json) => dispatchActionCreator(json.results, json.count));
}

export function fetchBookmarkedGroups(user: string,
                                      filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const groupsUrl = BASE_API_URL + `/bookmarks/${user}/groups/`;
    return _fetchGroups(groupsUrl, BOOKMARKS, filters, dispatch, getState);
  };
}

export function fetchArchivedGroups(user: string,
                                    filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const groupsUrl = BASE_API_URL + `/archives/${user}/groups/`;
    return _fetchGroups(groupsUrl, ARCHIVES, filters, dispatch, getState);
  };
}

export function fetchGroups(projectUniqueName: string,
                            filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const groupsUrl = `${BASE_API_URL}/${urlifyProjectName(projectUniqueName)}/groups/`;
    return _fetchGroups(groupsUrl, '', filters, dispatch, getState);
  };
}

export function fetchGroup(user: string, projectName: string, groupId: number): any {
  const groupUrl = getGroupUrl(user, projectName, groupId, false);
  return (dispatch: any, getState: any) => {
    dispatch(requestGroupsActionCreator());
    return fetch(`${BASE_API_URL}${groupUrl}`, {
      headers: {
        Authorization: 'token ' + getState().auth.token
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.json())
      .then((json) => dispatch(receiveGroupActionCreator(json)));
  };
}

export function updateGroup(groupName: string, updateDict: { [key: string]: any }): any {
  const groupUrl = getGroupUrlFromName(groupName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${groupUrl}`, {
        method: 'PATCH',
        body: JSON.stringify(updateDict),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.json())
      .then((json) => dispatch(updateGroupActionCreator(json)));
  };
}

export function updateSelection(groupName: string, updateDict: { [key: string]: any }): any {
  const selectionUrl = getSelectionUrlFromName(groupName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${selectionUrl}`, {
        method: 'PATCH',
        body: JSON.stringify(updateDict),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => {
        if ('operation' in updateDict && updateDict.operation === 'remove') {
          return dispatch(
            deleteExperimentsActionCreator(getProjectNameFromUniqueName(groupName), updateDict.experiment_ids)
          );
        }
      });
  };
}

export function deleteGroup(groupName: string, redirect: boolean = false): any {
  const groupUrl = getGroupUrlFromName(groupName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${groupUrl}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => {
        const dispatched = dispatch(deleteGroupActionCreator(groupName));
        if (redirect) {
          const values = groupName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#group');
        }
        return dispatched;
      });
  };
}

export function createGroup(projectName: string, body: { [key: string]: any }): any {
  const projectUrl = getProjectUrlFromName(projectName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${projectUrl}/groups`, {
        method: 'POST',
        body: JSON.stringify(body),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.json())
      .then((json) => dispatch(createGroupActionCreator(json)));
  };
}

export function archiveGroup(groupName: string, redirect: boolean = false): any {
  const groupUrl = getGroupUrlFromName(groupName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${groupUrl}/archive`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => {
        const dispatched = dispatch(archiveGroupActionCreator(groupName));
        if (redirect) {
          const values = groupName.split('.');
          history.push(getProjectUrl(values[0], values[1], true) + '#group');
        }
        return dispatched;
      });
  };
}

export function restoreGroup(groupName: string): any {
  const groupUrl = getGroupUrlFromName(groupName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${groupUrl}/restore`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(restoreGroupActionCreator(groupName)));
  };
}

export function stopGroup(groupName: string): any {
  const groupUrl = getGroupUrlFromName(groupName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${groupUrl}/stop`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(stopGroupActionCreator(groupName)));
  };
}

export function bookmark(groupName: string): any {
  const groupUrl = getGroupUrlFromName(groupName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${groupUrl}/bookmark`, {
        method: 'POST',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(bookmarkGroupActionCreator(groupName)));
  };
}

export function unbookmark(groupName: string): any {
  const groupUrl = getGroupUrlFromName(groupName, false);
  return (dispatch: any, getState: any) => {
    return fetch(
      `${BASE_API_URL}${groupUrl}/unbookmark`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'token ' + getState().auth.token,
          'X-CSRFToken': getState().auth.csrftoken
        },
      })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(unbookmarkGroupActionCreator(groupName)));
  };
}

export function startTensorboard(groupName: string): any {
  const groupUrl = getGroupUrlFromName(groupName, false);
  return (dispatch: any, getState: any) => {
    return fetch(`${BASE_API_URL}${groupUrl}/tensorboard/start`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(startGroupTensorboardActionCreator(groupName)));
  };
}

export function stopTensorboard(groupName: string): any {
  const groupUrl = getGroupUrlFromName(groupName, false);
  return (dispatch: any, getState: any) => {
    return fetch(`${BASE_API_URL}${groupUrl}/tensorboard/stop`, {
      method: 'POST',
      headers: {
        'Authorization': 'token ' + getState().auth.token,
        'X-CSRFToken': getState().auth.csrftoken
      }
    })
      .then((response) => handleAuthError(response, dispatch))
      .then(() => dispatch(stopGroupTensorboardActionCreator(groupName)));
  };
}
