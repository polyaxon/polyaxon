import { Reducer } from 'redux';
import { normalize } from 'normalizr';
import * as _ from 'lodash';

import { ProjectSchema } from '../constants/schemas';
import { ProjectAction, actionTypes } from '../actions/project';
import { ProjectStateSchema, ProjectsEmptyState, ProjectModel } from '../models/project';
import { UserEmptyState, UserModel, UserStateSchema } from '../models/user';
import { LastFetched } from '../models/utils';

export const projectsReducer: Reducer<ProjectStateSchema> =
  (state: ProjectStateSchema = ProjectsEmptyState, action: ProjectAction) => {
    let newState = {...state};

    let processProject = function(project: ProjectModel) {
      let uniqueName = project.unique_name;
      newState.lastFetched.names.push(uniqueName);
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
      if (newState.byUniqueNames[uniqueName].jobs == null) {
        newState.byUniqueNames[uniqueName].jobs = [];
      }
      if (newState.byUniqueNames[uniqueName].builds == null) {
        newState.byUniqueNames[uniqueName].builds = [];
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
      case actionTypes.REQUEST_PROJECTS:
        newState.lastFetched = new LastFetched();
        return newState;
      case actionTypes.RECEIVE_PROJECTS:
        newState.lastFetched = new LastFetched();
        newState.lastFetched.count = action.count;
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

export const UserProjectsReducer: Reducer<UserStateSchema> =
  (state: UserStateSchema = UserEmptyState, action: ProjectAction) => {
    let newState = {...state};

    let processProject = function (project: ProjectModel, count?: number) {
      let username = project.user;
      let uniqueName = project.unique_name;
      if (!_.includes(newState.userNames, username)) {
        newState.userNames.push(username);
        newState.byUserNames[username] = new UserModel();
      }
      if (!_.includes(newState.byUserNames[username].projects, uniqueName)) {
        newState.byUserNames[username].projects.push(uniqueName);
      }
      if (count != null) {
        newState.byUserNames[username].num_projects = count;
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.RECEIVE_PROJECT:
        return processProject(action.project);
      case actionTypes.RECEIVE_PROJECTS:
        for (let experiment of action.projects) {
          newState = processProject(experiment, action.count);
        }
        return newState;
      default:
        return state;
    }
  };
