import { Action } from 'redux';
import * as url from 'url';

import { BASE_API_URL } from '../../constants/api';
import history from '../../history';
import { BookmarkModel } from '../../models/bookmark';
import { ProjectModel } from '../../models/project';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';
import { stdFetchHandleError } from '../utils';
import { actionTypes } from './actionTypes';

export interface FetchProjectsRequestAction extends Action {
  type: actionTypes.FETCH_PROJECTS_REQUEST;
}

export interface FetchProjectsSuccessAction extends Action {
  type: actionTypes.FETCH_PROJECTS_SUCCESS;
  projects: ProjectModel[];
  count: number;
}

export interface FetchProjectsErrorAction extends Action {
  type: actionTypes.FETCH_PROJECTS_ERROR;
  statusCode: number;
  error: any;
}

export function getProjectsRequestActionCreator(): FetchProjectsRequestAction {
  return {
    type: actionTypes.FETCH_PROJECTS_REQUEST,
  };
}

export function fetchProjectsSuccessActionCreator(projects: ProjectModel[], count: number): FetchProjectsSuccessAction {
  return {
    type: actionTypes.FETCH_PROJECTS_SUCCESS,
    projects,
    count,
  };
}

export function fetchProjectsErrorActionCreator(statusCode: number, error: any): FetchProjectsErrorAction {
  return {
    type: actionTypes.FETCH_PROJECTS_ERROR,
    statusCode,
    error,
  };
}

export function fetchBookmarkedProjectsSuccessActionCreator(bookmarkedProjects: BookmarkModel[],
                                                            count: number): FetchProjectsSuccessAction {
  const projects: ProjectModel[] = [];
  for (const bookmarkedProject of bookmarkedProjects) {
    projects.push(bookmarkedProject.content_object as ProjectModel);
  }
  return {
    type: actionTypes.FETCH_PROJECTS_SUCCESS,
    projects,
    count,
  };
}

export type FetchProjectAction =
  FetchProjectsRequestAction
  | FetchProjectsSuccessAction
  | FetchProjectsErrorAction;

function _fetchProjects(projectsUrl: string,
                        endpointList: string,
                        filters: { [key: string]: number | boolean | string } = {},
                        dispatch: any,
                        getState: any): any {

  dispatch(getProjectsRequestActionCreator());

  const urlPieces = location.hash.split('?');
  const baseUrl = urlPieces[0];
  if (Object.keys(filters).length) {
    projectsUrl += url.format({query: filters});
    if (baseUrl) {
      history.push(baseUrl + url.format({query: filters}));
    }
  } else if (urlPieces.length > 1) {
    history.push(baseUrl);
  }

  const dispatchActionCreator = (results: any, count: number) => {
    if (endpointList === BOOKMARKS) {
      return dispatch(fetchBookmarkedProjectsSuccessActionCreator(results, count));
    } else {
      return dispatch(fetchProjectsSuccessActionCreator(results, count));
    }
  };

  return fetch(projectsUrl, {
    headers: {
      Authorization: 'token ' + getState().auth.token
    }
  })
    .then((response) => stdFetchHandleError(
      response,
      dispatch,
      fetchProjectsErrorActionCreator,
      'Projects not found',
      'Failed to fetch projects'))
    .then((response) => response.json())
    .then((json) => dispatchActionCreator(json.results, json.count))
    .catch((error) => undefined)
    .catch((response) => {
      if (response.status === 400) {
        return response.value.json().then(
          (value: any) => dispatch(fetchProjectsErrorActionCreator(response.status, value)));
      } else {
        return response.value;
      }
    });
}

export function fetchBookmarkedProjects(user: string,
                                        filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const projectsUrl = `${BASE_API_URL}/bookmarks/${user}/projects`;
    return _fetchProjects(projectsUrl, BOOKMARKS, filters, dispatch, getState);
  };
}

export function fetchArchivedProjects(user: string,
                                      filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const projectsUrl = `${BASE_API_URL}/archives/${user}/projects`;
    return _fetchProjects(projectsUrl, ARCHIVES, filters, dispatch, getState);
  };
}

export function fetchProjects(user: string,
                              filters: { [key: string]: number | boolean | string } = {}): any {
  return (dispatch: any, getState: any) => {
    const projectsUrl = `${BASE_API_URL}/${user}`;

    return _fetchProjects(projectsUrl, '', filters, dispatch, getState);
  };
}
