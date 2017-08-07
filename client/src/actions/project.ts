import {Action, Dispatch} from "redux";

import {ProjectModel} from "../models/project";
import {PROJECTS_URL} from "../constants/api";


export enum actionTypes {
  CREATE_PROJECT='CREATE_PROJECT',
  DELETE_PROJECT='DELETE_PROJECT',
  UPDATE_PROJECT='UPDATE_PROJECT',
  RECEIVE_PROJECTS='RECEIVE_PROJECTS',
  REQUEST_PROJECTS='REQUEST_PROJECTS',
}


export interface CreateUpdateProjectAction extends Action {
  type: actionTypes.CREATE_PROJECT | actionTypes.UPDATE_PROJECT;
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
  type: actionTypes.REQUEST_PROJECTS;
}

export type ProjectAction = CreateUpdateProjectAction | DeleteProjectAction | ReceiveProjects | RequestProjects;

export function createProject(project: ProjectModel): CreateUpdateProjectAction {
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

export function updateProject(project: ProjectModel): CreateUpdateProjectAction {
    return {
      type: actionTypes.UPDATE_PROJECT,
      project
    }
}


export function requestProjects(): RequestProjects {
  return {
    type: actionTypes.REQUEST_PROJECTS,
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

