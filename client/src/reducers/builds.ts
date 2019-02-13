import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, BuildAction } from '../actions/build';
import { BuildSchema } from '../constants/schemas';
import { STOPPED } from '../constants/statuses';
import { BuildModel, BuildsEmptyState, BuildStateSchema } from '../models/build';
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
      case actionTypes.CREATE_BUILD:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.build.unique_name]: action.build},
          uniqueNames: [...state.uniqueNames, action.build.unique_name]
        };
      case actionTypes.DELETE_BUILD:
        return {
          ...state,
          uniqueNames: state.uniqueNames.filter(
            (name) => name !== action.buildName),
          lastFetched: {
            ...state.lastFetched,
            names: state.lastFetched.names.filter((name) => name !== action.buildName)
          },
        };
      case actionTypes.ARCHIVE_BUILD:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.buildName]: {
              ...state.byUniqueNames[action.buildName], deleted: true
            }
          },
        };
      case actionTypes.RESTORE_BUILD:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.buildName]: {
              ...state.byUniqueNames[action.buildName], deleted: false
            }
          },
        };
      case actionTypes.STOP_BUILD:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.buildName]: {
              ...state.byUniqueNames[action.buildName], last_status: STOPPED
            }
          },
        };
      case actionTypes.BOOKMARK_BUILD:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.buildName]: {
              ...state.byUniqueNames[action.buildName], bookmarked: true
            }
          },
        };
      case actionTypes.UNBOOKMARK_BUILD:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.buildName]: {
              ...state.byUniqueNames[action.buildName], bookmarked: false
            }
          },
        };
      case actionTypes.UPDATE_BUILD:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.build.unique_name]: action.build}
        };
      case actionTypes.REQUEST_BUILDS:
        newState.lastFetched = new LastFetchedNames();
        return newState;
      case actionTypes.RECEIVE_BUILDS:
        newState.lastFetched = new LastFetchedNames();
        newState.lastFetched.count = action.count;
        for (const build of action.builds) {
          newState = processBuild(build);
        }
        return newState;
      case actionTypes.RECEIVE_BUILD:
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
      case actionTypes.RECEIVE_BUILD:
        return processBuild(action.build);
      case actionTypes.RECEIVE_BUILDS:
        for (const build of action.builds) {
          newState = processBuild(build);
        }
        return newState;
      default:
        return state;
    }
  };
