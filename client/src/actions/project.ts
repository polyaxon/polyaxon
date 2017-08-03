import {Action} from "redux";
import {ProjectModel} from "../models/project";


export enum actionTypes {
  CREATE_PROJECT='CREATE_PROJECT',
  DELETE_PROJECT='DELETE_PROJECT',
  UPDATE_PROJECT='UPDATE_PROJECT',
}


export interface CreateUpdateProjectAction extends Action {
  type: actionTypes.CREATE_PROJECT | actionTypes.UPDATE_PROJECT;
  project: ProjectModel
}

export interface DeleteProjectAction extends Action {
  type: actionTypes.DELETE_PROJECT;
  projectId: number
}

export type ProjectAction = CreateUpdateProjectAction | DeleteProjectAction;

export function createProject(project: ProjectModel): ProjectAction {
    return {
      type: actionTypes.CREATE_PROJECT,
      project
    }
}

export function deleteProject(projectId: number): ProjectAction {
    return {
      type: actionTypes.DELETE_PROJECT,
      projectId
    }
}

export function updateProject(project: ProjectModel): ProjectAction {
    return {
      type: actionTypes.UPDATE_PROJECT,
      project
    }
}
