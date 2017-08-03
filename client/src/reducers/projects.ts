import {Reducer} from "redux";
import {ProjectAction, actionTypes} from "../actions/project";
import {ProjectModel} from "../models/project";

export const projectsReducer: Reducer<ProjectModel[]> =
	(state: ProjectModel[] = [
	  {id: Math.floor(Math.random() * 60) + 1  , name: 'name'},
    {id: Math.floor(Math.random() * 60) + 1  , name: 'babla'}] as ProjectModel[],
  action: ProjectAction) => {

  switch (action.type) {
    case actionTypes.CREATE_PROJECT:
      return [...state, action.project];
    case actionTypes.DELETE_PROJECT:
      return state.filter(project => project.id != action.projectId);
    case actionTypes.UPDATE_PROJECT:
      return state.map(project => project.id === action.project.id? action.project: project);
  }
  return state;
};
