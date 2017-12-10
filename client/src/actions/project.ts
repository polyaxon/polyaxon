import {Action, Dispatch} from "redux";
import * as _ from "lodash";

import {ProjectModel} from "../models/project";
import {PROJECTS_URL} from "../constants/api";


export enum actionTypes {
  CREATE_PROJECT='CREATE_PROJECT',
  DELETE_PROJECT='DELETE_PROJECT',
  UPDATE_PROJECT='UPDATE_PROJECT',
  RECEIVE_PROJECT='RECEIVE_PROJECT',
  REQUEST_PROJECT='REQUEST_PROJECT',
  RECEIVE_PROJECTS='RECEIVE_PROJECTS',
  REQUEST_PROJECTS='REQUEST_PROJECTS',
}


export interface CreateUpdateReceiveProjectAction extends Action {
  type: actionTypes.CREATE_PROJECT | actionTypes.UPDATE_PROJECT | actionTypes.RECEIVE_PROJECT;
  project: ProjectModel
}

export interface DeleteProjectAction extends Action {
  type: actionTypes.DELETE_PROJECT;
  projectUuid: string
}

export interface ReceiveProjectsAction extends Action {
  type: actionTypes.RECEIVE_PROJECTS;
  projects: ProjectModel[]
}

export interface RequestProjectsAction extends Action {
  type: actionTypes.REQUEST_PROJECTS | actionTypes.REQUEST_PROJECT;
}

export type ProjectAction = CreateUpdateReceiveProjectAction | DeleteProjectAction | ReceiveProjectsAction | RequestProjectsAction;

export function createProjectActionCreator(project: ProjectModel): CreateUpdateReceiveProjectAction {
    return {
      type: actionTypes.CREATE_PROJECT,
      project
    }
}

export function deleteProjectActionCreator(projectUuid: string): DeleteProjectAction {
    return {
      type: actionTypes.DELETE_PROJECT,
      projectUuid
    }
}

export function updateProjectActionCreator(project: ProjectModel): CreateUpdateReceiveProjectAction {
    return {
      type: actionTypes.UPDATE_PROJECT,
      project
    }
}


export function requestProjectActionCreator(): RequestProjectsAction {
  return {
    type: actionTypes.REQUEST_PROJECT,
  }
}

export function requestProjectsActionCreator(): RequestProjectsAction {
  return {
    type: actionTypes.REQUEST_PROJECTS,
  }
}

export function receiveProjectActionCreator(project: ProjectModel): CreateUpdateReceiveProjectAction {
  return {
    type: actionTypes.RECEIVE_PROJECT,
    project
  }
}

export function receiveProjectsActionCreator(projects: ProjectModel[]): ReceiveProjectsAction {
  return {
    type: actionTypes.RECEIVE_PROJECTS,
    projects
  }
}


export function createProject(project: ProjectModel): Dispatch<ProjectModel> {
  return (dispatch: any) => {
    dispatch(createProjectActionCreator(project));
    return fetch(PROJECTS_URL, {
        method: 'POST',
        body: JSON.stringify(project),
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Authorization': 'token 8ff04973157b2a5831329fbb1befd37f93e4de4f'
        }
    })
    .then(() => dispatch(receiveProjectActionCreator(project)))
  }
}


export function deleteProject(projectUuid: string): Dispatch<ProjectModel[]> {
  return (dispatch: any) => {
    dispatch(deleteProjectActionCreator(projectUuid));
    return fetch(PROJECTS_URL + projectUuid, {
        method: 'DELETE',
        headers: {
            'Authorization': 'token 8ff04973157b2a5831329fbb1befd37f93e4de4f'
        }
    })
    .then(() => dispatch(receiveProjectsActionCreator([])))
  }
}


export function fetchProjects(): Dispatch<ProjectModel[]> {
  return (dispatch: any) => {
    dispatch(requestProjectsActionCreator());
    return fetch(PROJECTS_URL)
      .then(response => response.json())
      .then(json => json.results.map((project: {[key: string]: any}) => {
          return {
            ...project,
            createdAt: new Date(_.toString(project.created_at)),
            updatedAt: new Date(_.toString(project.updated_at))};
      }))
      .then(json => dispatch(receiveProjectsActionCreator(json)))
  }
}


export function fetchProject(projectUuid: string): Dispatch<ProjectModel> {
  return (dispatch: any) => {
    dispatch(requestProjectActionCreator());
    return fetch(PROJECTS_URL + projectUuid)
      .then(response => response.json())
      .then(json => {
          return {
            ...json,
            createdAt: new Date(_.toString(json.createdAt)),
            updatedAt: new Date(_.toString(json.updatedAt))};
        }
      )
      .then(json => dispatch(receiveProjectActionCreator(json)))
  }
}

