import {Action} from "redux";
import {ProjectModel} from "../models/project";


export enum actionTypes {
  CREATE_PROJECT,
  DELETE_PROJECT,
  UPDATE_PROJECT
}


export interface ProjectAction extends Action {
	project: ProjectModel;
}


export function createProject(): ProjectAction {
    return {
      type: actionTypes.CREATE_PROJECT,
      project: {id:1, name:'lol', description:'sdf', isPrivate:true} as ProjectModel
    }
}

export function deleteProject(): ProjectAction {
    return {
      type: actionTypes.DELETE_PROJECT,
      project: {id:1, name:'lol', description:'sdf', isPrivate:true} as ProjectModel
    }
}

export function updateProject(): ProjectAction {
    return {
      type: actionTypes.UPDATE_PROJECT,
      project: {id:1, name:'lol', description:'sdf', isPrivate:true} as ProjectModel
    }
}
