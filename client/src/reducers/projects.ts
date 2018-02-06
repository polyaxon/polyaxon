import { Reducer } from 'redux';
import { normalize } from 'normalizr';
import * as _ from 'lodash';

import { ProjectSchema } from '../constants/schemas';
import { ProjectAction, actionTypes } from '../actions/project';
import { ProjectStateSchema, ProjectsEmptyState, ProjectModel } from '../models/project';

export const projectsReducer: Reducer<ProjectStateSchema> =
  (state: ProjectStateSchema = ProjectsEmptyState, action: ProjectAction) => {
    let newState = {...state};

    let processProject = function(project: ProjectModel) {
      let uniqueName = project.unique_name;
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      let normalizedProjects = normalize(project, ProjectSchema).entities.projects;
      newState.byUniqueNames[uniqueName] = {
        ...newState.byUniqueNames[uniqueName], ...normalizedProjects[uniqueName]
      };
      if (newState.byUniqueNames[uniqueName].experiments == null) {
        newState.byUniqueNames[uniqueName].experiments = [];
      }
      if (newState.byUniqueNames[uniqueName].groups == null) {
        newState.byUniqueNames[uniqueName].groups = [];
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.CREATE_PROJECT:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.project.unique_name]: action.project},
          uniqueNames: [...state.uniqueNames, action.project.unique_name]
        };
      case actionTypes.DELETE_PROJECT:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.project.unique_name]: {
              ...state.byUniqueNames[action.project.unique_name], deleted: true
            }
          },
          uniqueNames: state.uniqueNames.filter(
            name => name !== action.project.unique_name),
        };
      case actionTypes.UPDATE_PROJECT:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.project.unique_name]: action.project}
        };
      case actionTypes.RECEIVE_PROJECTS:
        for (let project of action.projects) {
          newState = processProject(project);
        }
        return newState;
      case actionTypes.RECEIVE_PROJECT:
        return processProject(action.project);
      default:
        return state;
    }
  };
