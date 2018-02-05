import {Reducer} from "redux";
import {normalize} from 'normalizr';
import * as _ from "lodash";

import {ProjectSchema} from "../constants/schemas"
import {ProjectAction, actionTypes} from "../actions/project";
import {ProjectStateSchema, ProjectsEmptyState} from "../models/project";
import {ExperimentStateSchema, ExperimentsEmptyState} from "../models/experiment";

export const projectsReducer: Reducer<ProjectStateSchema> =
	(state: ProjectStateSchema = ProjectsEmptyState, action: ProjectAction) => {

  switch (action.type) {
    case actionTypes.CREATE_PROJECT:
      return {
        ...state,
        ByUniqueNames: {...state.ByUniqueNames, [action.project.unique_name] : action.project},
        uniqueNames: [...state.uniqueNames, action.project.unique_name]
      };
    case actionTypes.DELETE_PROJECT:
      return {
        ...state,
        ByUniqueNames: {
          ...state.ByUniqueNames,
          [action.project.unique_name] : {
            ...state.ByUniqueNames[action.project.unique_name], deleted:true}},
        uniqueNames: state.uniqueNames.filter(
          uniqueName => uniqueName != action.project.unique_name),
      };
    case actionTypes.UPDATE_PROJECT:
      return {
        ...state,
        ByUniqueNames: {...state.ByUniqueNames, [action.project.unique_name]: action.project}
      };
    case actionTypes.RECEIVE_PROJECTS:
      var newState = {...state};
      for (let project of action.projects) {
        if (!_.includes(newState.uniqueNames, project.unique_name)) {
          newState.uniqueNames.push(project.unique_name);
        }
        newState.ByUniqueNames[project.unique_name] = project;
      }
      return newState;
    case actionTypes.RECEIVE_PROJECT:
      var newState = {...state};
      let uniqueName = action.project.unique_name;
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      let normalized_projects = normalize(action.project, ProjectSchema).entities.projects;
      newState.ByUniqueNames[uniqueName] = normalized_projects[uniqueName];
      return newState;
  }
  return state;
};

export const ProjectExperiments: Reducer<ExperimentStateSchema> =
	(state: ExperimentStateSchema = ExperimentsEmptyState, action: ProjectAction) => {

  switch (action.type) {
    case actionTypes.RECEIVE_PROJECT:
      var newState = {...state};
      let normalized_project = normalize(action.project, ProjectSchema);
      let projectExperiments = normalized_project.entities.experiments;
      if (_.isNil(projectExperiments)) {
        return {ByUniqueNames: {}, uniqueNames: []};
      }
      for (let uniqueName of Object.keys(projectExperiments)) {
        if (!_.includes(newState.uniqueNames, uniqueName)) {
          newState.uniqueNames.push(uniqueName);
          newState.ByUniqueNames[uniqueName] = projectExperiments[uniqueName];
        }
      }
      return newState;
  }
  return state;
};
