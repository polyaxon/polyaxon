import { Reducer } from 'redux';
import { normalize } from 'normalizr';

import * as _ from 'lodash';

import { BuildSchema } from '../constants/schemas';
import { BuildAction, actionTypes } from '../actions/build';
import { BuildStateSchema, BuildsEmptyState, BuildModel } from '../models/build';
import { ProjectsEmptyState, ProjectStateSchema } from '../models/project';
import { LastFetchedNames } from '../models/utils';

export const buildsReducer: Reducer<BuildStateSchema> =
  (state: BuildStateSchema = BuildsEmptyState, action: BuildAction) => {
    let newState = {...state};

    let processBuild = function (build: BuildModel) {
      let uniqueName = build.unique_name;
      newState.lastFetched.names.push(uniqueName);
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      let normalizedBuilds = normalize(build, BuildSchema).entities.builds;
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
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.build.unique_name]: {
              ...state.byUniqueNames[action.build.unique_name], deleted: true}
          },
          uniqueNames: state.uniqueNames.filter(
            name => name !== action.build.unique_name),
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
        for (let build of action.builds) {
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

    let processBuild = function (build: BuildModel) {
      let uniqueName = build.unique_name;
      let projectName = build.project;
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
        for (let build of action.builds) {
          newState = processBuild(build);
        }
        return newState;
      default:
        return state;
    }
  };
