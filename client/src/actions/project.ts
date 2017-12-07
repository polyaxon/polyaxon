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

export function deleteProject(projectUuid: string): DeleteProjectAction {
    return {
      type: actionTypes.DELETE_PROJECT,
      projectUuid
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


export function generateProject(project: ProjectModel) {
  return (dispatch: any) => {
    dispatch(createProject(project));
    return fetch(PROJECTS_URL, {
        method: 'POST',
        body: JSON.stringify(project),
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        }
    })
  }
}


export function removeProject(projectUuid: string) {
  return (dispatch: any) => {
    dispatch(deleteProject(projectUuid));
    return fetch(PROJECTS_URL + projectUuid, {
        method: 'DELETE'
     })
  }
}


export function fetchProjects(): Dispatch<ProjectModel[]> {
  return (dispatch: any) => {
    dispatch(requestProjects());
    return fetch(PROJECTS_URL)
      .then(response => response.json())
      .then(json => json.results.map((project: ProjectModel) => {
          return {
            ...project,
            createdAt: new Date(_.toString(project.createdAt)),
            updatedAt: new Date(_.toString(project.updatedAt))};
      }))
      .then(json => dispatch(receiveProjects(json)))
  }
}



export function fetchProject(projectUuid: string): Dispatch<ProjectModel> {
  return (dispatch: any) => {
    dispatch(requestProject());
    return fetch(PROJECTS_URL + projectUuid)
      .then(response => response.json())
      .then(json => {
          return {
            ...json,
            createdAt: new Date(_.toString(json.createdAt)),
            updatedAt: new Date(_.toString(json.updatedAt))};
        }
      )
      .then(json => dispatch(receiveProject(json)))
  }
}

