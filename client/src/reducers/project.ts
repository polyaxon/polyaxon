import {Reducer} from 'redux';
import {actionTypes, ProjectAction} from '../actions/project';
import {ProjectModel} from "../models/project";

export const projectReducer: Reducer<ProjectModel[]> =
	(state: ProjectModel[] = [], action: ProjectAction) => {

  switch (action.type) {
    case actionTypes.CREATE_PROJECT:
      return state;
    case actionTypes.DELETE_PROJECT:
      return state;
    case actionTypes.UPDATE_PROJECT:
      return state;
  }
  return state;
};
