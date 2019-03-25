import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, BuildAction } from '../actions/builds';
import { ACTIONS } from '../constants/actions';
import { BuildSchema } from '../constants/schemas';
import { STOPPED } from '../constants/statuses';
import { BuildModel, BuildsEmptyState, BuildStateSchema } from '../models/build';
import {
  LoadingIndicatorEmptyState,
  LoadingIndicatorSchema,
  processLoadingIndicatorById,
  processLoadingIndicatorGlobal
} from '../models/loadingIndicator';
import { ProjectsEmptyState, ProjectStateSchema } from '../models/project';
import { LastFetchedNames } from '../models/utils';

export const buildsReducer: Reducer<BuildStateSchema> =
  (state: BuildStateSchema = BuildsEmptyState, action: BuildAction) => {
    let newState = {...state};

    const processBuild = (build: BuildModel) => {
      const uniqueName = build.unique_name;
      if (!_.includes(newState.lastFetched.names, uniqueName)) {
        newState.lastFetched.names.push(uniqueName);
      }
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      if (_.isNil(build.deleted)) {
        build.deleted = false;
      }
      const normalizedBuilds = normalize(build, BuildSchema).entities.builds;
      newState.byUniqueNames[uniqueName] = {
        ...newState.byUniqueNames[uniqueName], ...normalizedBuilds[build.unique_name]
      };
      return newState;
    };

    switch (action.type) {
      case actionTypes.DELETE_BUILD_SUCCESS:
        return {
          ...state,
          uniqueNames: state.uniqueNames.filter(
            (name) => name !== action.buildName),
          lastFetched: {
            ...state.lastFetched,
            names: state.lastFetched.names.filter((name) => name !== action.buildName)
          },
        };
      case actionTypes.ARCHIVE_BUILD_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.buildName]: {
              ...state.byUniqueNames[action.buildName], deleted: true
            }
          },
        };
      case actionTypes.RESTORE_BUILD_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.buildName]: {
              ...state.byUniqueNames[action.buildName], deleted: false
            }
          },
        };
      case actionTypes.STOP_BUILD_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.buildName]: {
              ...state.byUniqueNames[action.buildName], last_status: STOPPED
            }
          },
        };
      case actionTypes.BOOKMARK_BUILD_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.buildName]: {
              ...state.byUniqueNames[action.buildName], bookmarked: true
            }
          },
        };
      case actionTypes.UNBOOKMARK_BUILD_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.buildName]: {
              ...state.byUniqueNames[action.buildName], bookmarked: false
            }
          },
        };
      case actionTypes.UPDATE_BUILD_SUCCESS:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.build.unique_name]: action.build}
        };
      case actionTypes.FETCH_BUILDS_REQUEST:
        newState.lastFetched = new LastFetchedNames();
        return newState;
      case actionTypes.FETCH_BUILDS_SUCCESS:
        newState.lastFetched = new LastFetchedNames();
        newState.lastFetched.count = action.count;
        for (const build of action.builds) {
          newState = processBuild(build);
        }
        return newState;
      case actionTypes.GET_BUILD_SUCCESS:
        return processBuild(action.build);
      default:
        return state;
    }
  };

export const ProjectBuildsReducer: Reducer<ProjectStateSchema> =
  (state: ProjectStateSchema = ProjectsEmptyState, action: BuildAction) => {
    let newState = {...state};

    const processBuild = (build: BuildModel) => {
      const uniqueName = build.unique_name;
      const projectName = build.project;
      if (_.includes(newState.uniqueNames, projectName) &&
        !_.includes(newState.byUniqueNames[projectName].builds, uniqueName)) {
        newState.byUniqueNames[projectName].builds.push(uniqueName);
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.GET_BUILD_SUCCESS:
        return processBuild(action.build);
      case actionTypes.FETCH_BUILDS_SUCCESS:
        for (const build of action.builds) {
          newState = processBuild(build);
        }
        return newState;
      default:
        return state;
    }
  };

export const LoadingIndicatorBuildReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: BuildAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_BUILD_REQUEST:
        return {
          ...state,
          builds: processLoadingIndicatorById(state.builds, action.buildName, true, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_BUILD_ERROR:
      case actionTypes.UPDATE_BUILD_SUCCESS:
        return {
          ...state,
          builds: processLoadingIndicatorById(state.builds, action.buildName, false, ACTIONS.UPDATE)
        };

      case actionTypes.GET_BUILD_REQUEST:
        return {
          ...state,
          builds: processLoadingIndicatorGlobal(
            processLoadingIndicatorById(state.builds, action.buildName, true, ACTIONS.GET),
            false,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_BUILD_ERROR:
      case actionTypes.GET_BUILD_SUCCESS:
        return {
          ...state,
          builds: processLoadingIndicatorById(state.builds, action.buildName, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_BUILD_REQUEST:
        return {
          ...state,
          builds: processLoadingIndicatorById(state.builds, action.buildName, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_BUILD_ERROR:
      case actionTypes.DELETE_BUILD_SUCCESS:
        return {
          ...state,
          builds: processLoadingIndicatorById(state.builds, action.buildName, false, ACTIONS.DELETE)
        };

      case actionTypes.ARCHIVE_BUILD_REQUEST:
        return {
          ...state,
          builds: processLoadingIndicatorById(state.builds, action.buildName, true, ACTIONS.ARCHIVE)
        };
      case actionTypes.ARCHIVE_BUILD_ERROR:
      case actionTypes.ARCHIVE_BUILD_SUCCESS:
        return {
          ...state,
          builds: processLoadingIndicatorById(state.builds, action.buildName, false, ACTIONS.ARCHIVE)
        };

      case actionTypes.RESTORE_BUILD_REQUEST:
        return {
          ...state,
          builds: processLoadingIndicatorById(state.builds, action.buildName, true, ACTIONS.RESTORE)
        };
      case actionTypes.RESTORE_BUILD_ERROR:
      case actionTypes.RESTORE_BUILD_SUCCESS:
        return {
          ...state,
          builds: processLoadingIndicatorById(state.builds, action.buildName, false, ACTIONS.RESTORE)
        };

       case actionTypes.STOP_BUILD_REQUEST:
        return {
          ...state,
          builds: processLoadingIndicatorById(state.builds, action.buildName, true, ACTIONS.STOP)
        };
      case actionTypes.STOP_BUILD_ERROR:
      case actionTypes.STOP_BUILD_SUCCESS:
        return {
          ...state,
          builds: processLoadingIndicatorById(state.builds, action.buildName, false, ACTIONS.STOP)
        };

      case actionTypes.BOOKMARK_BUILD_REQUEST:
        return {
          ...state,
          builds: processLoadingIndicatorById(state.builds, action.buildName, true, ACTIONS.BOOKMARK)
        };
      case actionTypes.BOOKMARK_BUILD_ERROR:
      case actionTypes.BOOKMARK_BUILD_SUCCESS:
        return {
          ...state,
          builds: processLoadingIndicatorById(state.builds, action.buildName, false, ACTIONS.BOOKMARK)
        };

      case actionTypes.UNBOOKMARK_BUILD_REQUEST:
        return {
          ...state,
          builds: processLoadingIndicatorById(state.builds, action.buildName, true, ACTIONS.UNBOOKMARK)
        };
      case actionTypes.UNBOOKMARK_BUILD_ERROR:
      case actionTypes.UNBOOKMARK_BUILD_SUCCESS:
        return {
          ...state,
          builds: processLoadingIndicatorById(state.builds, action.buildName, false, ACTIONS.UNBOOKMARK)
        };

      case actionTypes.FETCH_BUILDS_REQUEST:
        return {
          ...state,
          builds: processLoadingIndicatorGlobal(state.builds, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_BUILDS_ERROR:
      case actionTypes.FETCH_BUILDS_SUCCESS:
        return {
          ...state,
          builds: processLoadingIndicatorGlobal(state.builds, false, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_BUILD_REQUEST:
        return {
          ...state,
          builds: processLoadingIndicatorGlobal(state.builds, true, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_BUILD_ERROR:
        return {
          ...state,
          builds: processLoadingIndicatorGlobal(state.builds, false, ACTIONS.CREATE)
        };
      default:
        return state;
    }
  };
