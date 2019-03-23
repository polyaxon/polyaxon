import { Action } from 'redux';
import * as url from 'url';

import { BASE_API_URL } from '../../constants/api';
import { urlifyProjectName } from '../../constants/utils';
import history from '../../history';
import { BookmarkModel } from '../../models/bookmark';
import { GroupModel } from '../../models/group';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';
import { stdHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface FetchGroupsRequestAction extends Action {
  type: actionTypes.FETCH_GROUPS_REQUEST;
}

export interface FetchGroupsSuccessAction extends Action {
  type: actionTypes.FETCH_GROUPS_SUCCESS;
  groups: GroupModel[];
  count: number;
}

export interface FetchGroupsErrorAction extends Action {
  type: actionTypes.FETCH_GROUPS_ERROR;
}

export interface FetchGroupsErrorAction extends Action {
  type: actionTypes.FETCH_GROUPS_ERROR;
  statusCode: number;
  error: any;
}

export function fetchGroupsRequestActionCreator(): FetchGroupsRequestAction {
  return {
    type: actionTypes.FETCH_GROUPS_REQUEST,
  };
}

export function fetchGroupsSuccessActionCreator(groups: GroupModel[], count: number): FetchGroupsSuccessAction {
  return {
    type: actionTypes.FETCH_GROUPS_SUCCESS,
    groups,
    count
  };
}

export function fetchBookmarkedGroupsSuccessActionCreator(bookmarkedGroups: BookmarkModel[],
                                                          count: number): FetchGroupsSuccessAction {
  const groups: GroupModel[] = [];
  for (const bookmarkedGroup of bookmarkedGroups) {
    groups.push(bookmarkedGroup.content_object as GroupModel);
  }
  return {
    type: actionTypes.FETCH_GROUPS_SUCCESS,
    groups,
    count
  };
}

export function fetchGroupsErrorActionCreator(statusCode: number, error: any): FetchGroupsErrorAction {
  return {
    type: actionTypes.FETCH_GROUPS_ERROR,
    statusCode,
    error,
  };
}

export type FetchGroupAction =
  FetchGroupsRequestAction
  | FetchGroupsSuccessAction
  | FetchGroupsErrorAction;

function _fetchGroups(groupsUrl: string,
                      endpointList: string,
                      filters: { [key: string]: number | boolean | string } = {},
                      dispatch: any,
                      getState: any): any {

  dispatch(fetchGroupsRequestActionCreator());

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
      dispatch(fetchBookmarkedGroupsSuccessActionCreator(results, count));
    } else {
      dispatch(fetchGroupsSuccessActionCreator(results, count));
    }
  };

  return fetch(groupsUrl, {
    headers: {
      Authorization: 'token ' + getState().auth.token
    }
  })
    .then((response) => stdHandleError(
        response,
        dispatch,
        fetchGroupsErrorActionCreator,
        'Groups not found',
        'Failed to fetch groups'))
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
