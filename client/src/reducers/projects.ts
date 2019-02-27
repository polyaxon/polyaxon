import * as _ from 'lodash';
import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import { actionTypes, ProjectAction } from '../actions/project';
import { ProjectSchema } from '../constants/schemas';
import { ProjectModel, ProjectsEmptyState, ProjectStateSchema } from '../models/project';
import { UserEmptyState, UserModel, UserStateSchema } from '../models/user';
import { LastFetchedNames } from '../models/utils';

export const projectsReducer: Reducer<ProjectStateSchema> =
  (state: ProjectStateSchema = ProjectsEmptyState, action: ProjectAction) => {
    let newState = {...state};

    const setProjectRelated = (project: ProjectModel) => {
      if (project.experiments == null) {
        project.experiments = [];
      }
      if (project.groups == null) {
        project.groups = [];
      }
      if (project.jobs == null) {
        project.jobs = [];
      }
      if (project.builds == null) {
        project.builds = [];
      }
      return project;
    };

    const processProject = (project: ProjectModel) => {
      const uniqueName = project.unique_name;
      if (!_.includes(newState.lastFetched.names, uniqueName)) {
        newState.lastFetched.names.push(uniqueName);
      }
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      if (_.isNil(project.deleted)) {
        project.deleted = false;
      }
      const normalizedProjects = normalize(project, ProjectSchema).entities.projects;
      newState.byUniqueNames[uniqueName] = {
        ...newState.byUniqueNames[uniqueName], ...normalizedProjects[uniqueName]
      };
      setProjectRelated(newState.byUniqueNames[uniqueName]);
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
          uniqueNames: state.uniqueNames.filter(
            (name) => name !== action.projectName),
          lastFetched: {
            ...state.lastFetched,
            names: state.lastFetched.names.filter((name) => name !== action.projectName)
          },
        };
      case actionTypes.ARCHIVE_PROJECT:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.projectName]: {
              ...state.byUniqueNames[action.projectName], deleted: true}
          },
        };
      case actionTypes.RESTORE_PROJECT:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.projectName]: {
              ...state.byUniqueNames[action.projectName], deleted: false}
          },
        };
      case actionTypes.BOOKMARK_PROJECT:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.projectName]: {
              ...state.byUniqueNames[action.projectName], bookmarked: true}
          },
        };
      case actionTypes.UNBOOKMARK_PROJECT:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.projectName]: {
              ...state.byUniqueNames[action.projectName], bookmarked: false}
          },
        };
      case actionTypes.STOP_PROJECT_TENSORBOARD:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.projectName]: {
              ...state.byUniqueNames[action.projectName], has_tensorboard: false}
          },
        };
      case actionTypes.STOP_PROJECT_NOTEBOOK:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.projectName]: {
              ...state.byUniqueNames[action.projectName], has_notebook: false}
          },
        };
      case actionTypes.UPDATE_PROJECT:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.project.unique_name]: setProjectRelated(action.project)}
        };
      case actionTypes.REQUEST_PROJECTS:
        newState.lastFetched = new LastFetchedNames();
        return newState;
      case actionTypes.RECEIVE_PROJECTS:
        newState.lastFetched = new LastFetchedNames();
        newState.lastFetched.count = action.count;
        for (const project of action.projects) {
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

    const processProject = (project: ProjectModel, count?: number) => {
      const username = project.user;
      const uniqueName = project.unique_name;
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
        for (const experiment of action.projects) {
          newState = processProject(experiment, action.count);
        }
        return newState;
      default:
        return state;
    }
  };
