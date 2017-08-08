import {Action, Dispatch} from "redux";

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
  projectId: number
}

export interface ReceiveProjects extends Action {
  type: actionTypes.RECEIVE_PROJECTS;
  projects: ProjectModel[]
}

export interface RequestProjects extends Action {
  type: actionTypes.REQUEST_PROJECTS | actionTypes.REQUEST_PROJECT;
}

export type ProjectAction = CreateUpdateReceiveProjectAction | DeleteProjectAction | ReceiveProjects | RequestProjects;

export function createProject(project: ProjectModel): CreateUpdateReceiveProjectAction {
    return {
      type: actionTypes.CREATE_PROJECT,
      project
    }
}

export function deleteProject(projectId: number): DeleteProjectAction {
    return {
      type: actionTypes.DELETE_PROJECT,
      projectId
    }
}

export function updateProject(project: ProjectModel): CreateUpdateReceiveProjectAction {
    return {
      type: actionTypes.UPDATE_PROJECT,
      project
    }
}


export function requestProject(): RequestProjects {
  return {
    type: actionTypes.REQUEST_PROJECT,
  }
}

export function requestProjects(): RequestProjects {
  return {
    type: actionTypes.REQUEST_PROJECTS,
  }
}

export function receiveProject(project: ProjectModel): CreateUpdateReceiveProjectAction {
  return {
    type: actionTypes.RECEIVE_PROJECT,
    project
  }
}

export function receiveProjects(projects: ProjectModel[]): ReceiveProjects {
  return {
    type: actionTypes.RECEIVE_PROJECTS,
    projects
  }
}


export function fetchProjects(): Dispatch<ProjectModel[]> {
  return dispatch => {
    dispatch(requestProjects());
    return fetch(PROJECTS_URL)
      .then(response => response.json())
      .then(json => json.map(project => {
          return {...project, createdAt: new Date(project.createdAt), updatedAt: new Date(project.updatedAt)};
        })
      )
      .then(json => dispatch(receiveProjects(json)))
  }
}


export function fetchProject(projectId: number): Dispatch<ProjectModel> {
  return dispatch => {
    dispatch(requestProject());
    return fetch(PROJECTS_URL + projectId)
      .then(response => response.json())
      .then(json => {
          return {...json, createdAt: new Date(json.createdAt), updatedAt: new Date(json.updatedAt)};
        }
      )
      .then(json => dispatch(receiveProject(json)))
  }
}

