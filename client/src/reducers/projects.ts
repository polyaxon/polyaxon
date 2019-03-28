import * as _ from 'lodash';
import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import { actionTypes, ProjectAction } from '../actions/projects';
import { ACTIONS } from '../constants/actions';
import { ProjectSchema } from '../constants/schemas';
import { AlertEmptyState, AlertSchema, processErrorById, processErrorGlobal } from '../models/alerts';
import {
  LoadingIndicatorEmptyState,
  LoadingIndicatorSchema,
  processLoadingIndicatorById,
  processLoadingIndicatorGlobal
} from '../models/loadingIndicator';
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
      case actionTypes.DELETE_PROJECT_SUCCESS:
        return {
          ...state,
          uniqueNames: state.uniqueNames.filter(
            (name) => name !== action.projectName),
          lastFetched: {
            ...state.lastFetched,
            names: state.lastFetched.names.filter((name) => name !== action.projectName)
          },
        };
      case actionTypes.ARCHIVE_PROJECT_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.projectName]: {
              ...state.byUniqueNames[action.projectName], deleted: true
            }
          },
        };
      case actionTypes.RESTORE_PROJECT_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.projectName]: {
              ...state.byUniqueNames[action.projectName], deleted: false
            }
          },
        };
      case actionTypes.BOOKMARK_PROJECT_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.projectName]: {
              ...state.byUniqueNames[action.projectName], bookmarked: true
            }
          },
        };
      case actionTypes.UNBOOKMARK_PROJECT_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.projectName]: {
              ...state.byUniqueNames[action.projectName], bookmarked: false
            }
          },
        };
      case actionTypes.STOP_PROJECT_TENSORBOARD_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.projectName]: {
              ...state.byUniqueNames[action.projectName], has_tensorboard: false
            }
          },
        };
      case actionTypes.STOP_PROJECT_NOTEBOOK_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.projectName]: {
              ...state.byUniqueNames[action.projectName], has_notebook: false
            }
          },
        };
      case actionTypes.UPDATE_PROJECT_SUCCESS:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.project.unique_name]: setProjectRelated(action.project)}
        };
      case actionTypes.FETCH_PROJECTS_REQUEST:
        newState.lastFetched = new LastFetchedNames();
        return newState;
      case actionTypes.FETCH_PROJECTS_SUCCESS:
        newState.lastFetched = new LastFetchedNames();
        newState.lastFetched.count = action.count;
        for (const project of action.projects) {
          newState = processProject(project);
        }
        return newState;
      case actionTypes.GET_PROJECT_SUCCESS:
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
      case actionTypes.GET_PROJECT_SUCCESS:
        return processProject(action.project);
      case actionTypes.FETCH_PROJECTS_SUCCESS:
        for (const experiment of action.projects) {
          newState = processProject(experiment, action.count);
        }
        return newState;
      default:
        return state;
    }
  };

export const LoadingIndicatorProjectReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: ProjectAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_PROJECT_REQUEST:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, true, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_PROJECT_ERROR:
      case actionTypes.UPDATE_PROJECT_SUCCESS:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, false, ACTIONS.UPDATE)
        };

      case actionTypes.GET_PROJECT_REQUEST:
        return {
          ...state,
          projects: processLoadingIndicatorGlobal(
            processLoadingIndicatorById(state.projects, action.projectName, true, ACTIONS.GET),
            false,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_PROJECT_ERROR:
      case actionTypes.GET_PROJECT_SUCCESS:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_PROJECT_REQUEST:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_PROJECT_ERROR:
      case actionTypes.DELETE_PROJECT_SUCCESS:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, false, ACTIONS.DELETE)
        };

      case actionTypes.ARCHIVE_PROJECT_REQUEST:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, true, ACTIONS.ARCHIVE)
        };
      case actionTypes.ARCHIVE_PROJECT_ERROR:
      case actionTypes.ARCHIVE_PROJECT_SUCCESS:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, false, ACTIONS.ARCHIVE)
        };

      case actionTypes.RESTORE_PROJECT_REQUEST:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, true, ACTIONS.RESTORE)
        };
      case actionTypes.RESTORE_PROJECT_ERROR:
      case actionTypes.RESTORE_PROJECT_SUCCESS:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, false, ACTIONS.RESTORE)
        };

      case actionTypes.BOOKMARK_PROJECT_REQUEST:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, true, ACTIONS.BOOKMARK)
        };
      case actionTypes.BOOKMARK_PROJECT_ERROR:
      case actionTypes.BOOKMARK_PROJECT_SUCCESS:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, false, ACTIONS.BOOKMARK)
        };

      case actionTypes.UNBOOKMARK_PROJECT_REQUEST:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, true, ACTIONS.UNBOOKMARK)
        };
      case actionTypes.UNBOOKMARK_PROJECT_ERROR:
      case actionTypes.UNBOOKMARK_PROJECT_SUCCESS:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, false, ACTIONS.UNBOOKMARK)
        };

      case actionTypes.START_PROJECT_TENSORBOARD_REQUEST:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, true, ACTIONS.START_TENSORBOARD)
        };
      case actionTypes.START_PROJECT_TENSORBOARD_ERROR:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, false, ACTIONS.START_TENSORBOARD)
        };

      case actionTypes.STOP_PROJECT_TENSORBOARD_REQUEST:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, true, ACTIONS.STOP_TENSORBOARD)
        };
      case actionTypes.STOP_PROJECT_TENSORBOARD_ERROR:
      case actionTypes.STOP_PROJECT_TENSORBOARD_SUCCESS:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, false, ACTIONS.STOP_TENSORBOARD)
        };

      case actionTypes.START_PROJECT_NOTEBOOK_REQUEST:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, true, ACTIONS.START_NOTEBOOK)
        };
      case actionTypes.START_PROJECT_NOTEBOOK_ERROR:
      case actionTypes.START_PROJECT_NOTEBOOK_SUCCESS:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, false, ACTIONS.START_NOTEBOOK)
        };

      case actionTypes.STOP_PROJECT_NOTEBOOK_REQUEST:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, true, ACTIONS.STOP_NOTEBOOK)
        };
      case actionTypes.STOP_PROJECT_NOTEBOOK_ERROR:
      case actionTypes.STOP_PROJECT_NOTEBOOK_SUCCESS:
        return {
          ...state,
          projects: processLoadingIndicatorById(state.projects, action.projectName, false, ACTIONS.STOP_NOTEBOOK)
        };

      case actionTypes.FETCH_PROJECTS_REQUEST:
        return {
          ...state,
          projects: processLoadingIndicatorGlobal(state.projects, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_PROJECTS_ERROR:
      case actionTypes.FETCH_PROJECTS_SUCCESS:
        return {
          ...state,
          projects: processLoadingIndicatorGlobal(state.projects, false, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_PROJECT_REQUEST:
        return {
          ...state,
          projects: processLoadingIndicatorGlobal(state.projects, true, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_PROJECT_ERROR:
      case actionTypes.CREATE_PROJECT_SUCCESS:
        return {
          ...state,
          projects: processLoadingIndicatorGlobal(state.projects, false, ACTIONS.CREATE)
        };
      default:
        return state;
    }
  };

export const AlertProjectReducer: Reducer<AlertSchema> =
  (state: AlertSchema = AlertEmptyState, action: ProjectAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_PROJECT_REQUEST:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, null, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_PROJECT_SUCCESS:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, true, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_PROJECT_ERROR:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, action.error, false, ACTIONS.UPDATE)
        };

      case actionTypes.GET_PROJECT_REQUEST:
        return {
          ...state,
          projects: processErrorGlobal(
            processErrorById(state.projects, action.projectName, null, null, ACTIONS.GET),
            null,
            null,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_PROJECT_SUCCESS:
         return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, true, ACTIONS.GET)
        };
      case actionTypes.GET_PROJECT_ERROR:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, action.error, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_PROJECT_REQUEST:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, null, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_PROJECT_SUCCESS:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_PROJECT_ERROR:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, action.error, false, ACTIONS.DELETE)
        };

      case actionTypes.ARCHIVE_PROJECT_REQUEST:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, null, ACTIONS.ARCHIVE)
        };
      case actionTypes.ARCHIVE_PROJECT_SUCCESS:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, true, ACTIONS.ARCHIVE)
        };
      case actionTypes.ARCHIVE_PROJECT_ERROR:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, action.error, false, ACTIONS.ARCHIVE)
        };

      case actionTypes.RESTORE_PROJECT_REQUEST:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, null, ACTIONS.RESTORE)
        };
      case actionTypes.RESTORE_PROJECT_SUCCESS:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, true, ACTIONS.RESTORE)
        };
      case actionTypes.RESTORE_PROJECT_ERROR:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, action.error, false, ACTIONS.RESTORE)
        };

      case actionTypes.BOOKMARK_PROJECT_REQUEST:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, null, ACTIONS.BOOKMARK)
        };
      case actionTypes.BOOKMARK_PROJECT_SUCCESS:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, true, ACTIONS.BOOKMARK)
        };
      case actionTypes.BOOKMARK_PROJECT_ERROR:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, action.error, false, ACTIONS.BOOKMARK)
        };

      case actionTypes.UNBOOKMARK_PROJECT_REQUEST:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, null, ACTIONS.UNBOOKMARK)
        };
      case actionTypes.UNBOOKMARK_PROJECT_SUCCESS:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, true, ACTIONS.UNBOOKMARK)
        };
      case actionTypes.UNBOOKMARK_PROJECT_ERROR:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, action.error, false, ACTIONS.UNBOOKMARK)
        };

      case actionTypes.START_PROJECT_TENSORBOARD_REQUEST:
        return {
          ...state,
          projects: processErrorById(state.projects,
                                     action.projectName,
                                     null,
                                     null,
                                     ACTIONS.START_TENSORBOARD),
          tensorboards: processErrorGlobal(state.tensorboards, null, null, ACTIONS.CREATE)
        };
      case actionTypes.START_PROJECT_TENSORBOARD_SUCCESS:
        return {
          ...state,
          projects: processErrorById(state.projects,
                                     action.projectName,
                                     null,
                                     true,
                                     ACTIONS.START_TENSORBOARD),
          tensorboards: processErrorGlobal(state.tensorboards, null, true, ACTIONS.CREATE)
        };
      case actionTypes.START_PROJECT_TENSORBOARD_ERROR:
        return {
          ...state,
          projects: processErrorById(state.projects,
                                     action.projectName,
                                     action.error,
                                     false,
                                     ACTIONS.START_TENSORBOARD),
          tensorboards: processErrorGlobal(state.tensorboards, action.error, false, ACTIONS.CREATE)
        };

      case actionTypes.STOP_PROJECT_TENSORBOARD_REQUEST:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, null, ACTIONS.STOP_TENSORBOARD)
        };
      case actionTypes.STOP_PROJECT_TENSORBOARD_SUCCESS:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, true, ACTIONS.STOP_TENSORBOARD)
        };
      case actionTypes.STOP_PROJECT_TENSORBOARD_ERROR:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, action.error, false, ACTIONS.STOP_TENSORBOARD)
        };

      case actionTypes.START_PROJECT_NOTEBOOK_REQUEST:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, null, ACTIONS.START_NOTEBOOK),
          notebooks: processErrorGlobal(state.notebooks, null, null, ACTIONS.CREATE)
        };
      case actionTypes.START_PROJECT_NOTEBOOK_SUCCESS:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, true, ACTIONS.START_NOTEBOOK),
          notebooks: processErrorGlobal(state.notebooks, null, true, ACTIONS.CREATE)
        };
      case actionTypes.START_PROJECT_NOTEBOOK_ERROR:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, action.error, false, ACTIONS.START_NOTEBOOK),
          notebooks: processErrorGlobal(state.notebooks, action.error, false, ACTIONS.CREATE)
        };

      case actionTypes.STOP_PROJECT_NOTEBOOK_REQUEST:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, null, ACTIONS.STOP_NOTEBOOK)
        };
      case actionTypes.STOP_PROJECT_NOTEBOOK_SUCCESS:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, null, true, ACTIONS.STOP_NOTEBOOK)
        };
      case actionTypes.STOP_PROJECT_NOTEBOOK_ERROR:
        return {
          ...state,
          projects: processErrorById(state.projects, action.projectName, action.error, false, ACTIONS.STOP_NOTEBOOK)
        };

      case actionTypes.FETCH_PROJECTS_REQUEST:
        return {
          ...state,
          projects: processErrorGlobal(state.projects, null, null, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_PROJECTS_SUCCESS:
        return {
          ...state,
          projects: processErrorGlobal(state.projects, null, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_PROJECTS_ERROR:
        return {
          ...state,
          projects: processErrorGlobal(state.projects, action.error, false, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_PROJECT_REQUEST:
        return {
          ...state,
          projects: processErrorGlobal(state.projects, null, null, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_PROJECT_SUCCESS:
        return {
          ...state,
          projects: processErrorGlobal(state.projects, null, true, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_PROJECT_ERROR:
        return {
          ...state,
          projects: processErrorGlobal(state.projects, action.error, false, ACTIONS.CREATE)
        };
      default:
        return state;
    }
  };
