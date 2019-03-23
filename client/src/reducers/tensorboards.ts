import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, TensorboardAction } from '../actions/tensorboards';
import { TensorboardSchema } from '../constants/schemas';
import { STOPPED } from '../constants/statuses';
import { TensorboardModel, TensorboardsEmptyState, TensorboardStateSchema } from '../models/tensorboard';
import { LastFetchedNames } from '../models/utils';

export const tensorboardsReducer: Reducer<TensorboardStateSchema> =
  (state: TensorboardStateSchema = TensorboardsEmptyState, action: TensorboardAction) => {
    let newState = {...state};

    const processBuild = (tensorboard: TensorboardModel) => {
      const uniqueName = tensorboard.unique_name;
      if (!_.includes(newState.lastFetched.names, uniqueName)) {
        newState.lastFetched.names.push(uniqueName);
      }
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      if (_.isNil(tensorboard.deleted)) {
        tensorboard.deleted = false;
      }
      const normalizedBuilds = normalize(tensorboard, TensorboardSchema).entities.tensorboards;
      newState.byUniqueNames[uniqueName] = {
        ...newState.byUniqueNames[uniqueName], ...normalizedBuilds[tensorboard.unique_name]
      };
      return newState;
    };

    switch (action.type) {
      case actionTypes.DELETE_TENSORBOARD_SUCCESS:
        return {
          ...state,
          uniqueNames: state.uniqueNames.filter(
            (name) => name !== action.tensorboardName),
          lastFetched: {
            ...state.lastFetched,
            names: state.lastFetched.names.filter((name) => name !== action.tensorboardName)
          },
        };
      case actionTypes.ARCHIVE_TENSORBOARD_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.tensorboardName]: {
              ...state.byUniqueNames[action.tensorboardName], deleted: true
            }
          },
        };
      case actionTypes.RESTORE_TENSORBOARD_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.tensorboardName]: {
              ...state.byUniqueNames[action.tensorboardName], deleted: false
            }
          },
        };
      case actionTypes.STOP_TENSORBOARD_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.tensorboardName]: {
              ...state.byUniqueNames[action.tensorboardName], last_status: STOPPED
            }
          },
        };
      case actionTypes.BOOKMARK_TENSORBOARD_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.tensorboardName]: {
              ...state.byUniqueNames[action.tensorboardName], bookmarked: true
            }
          },
        };
      case actionTypes.UNBOOKMARK_TENSORBOARD_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.tensorboardName]: {
              ...state.byUniqueNames[action.tensorboardName], bookmarked: false
            }
          },
        };
      case actionTypes.UPDATE_TENSORBOARD_SUCCESS:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.tensorboard.unique_name]: action.tensorboard}
        };
      case actionTypes.FETCH_TENSORBOARDS_REQUEST:
        newState.lastFetched = new LastFetchedNames();
        return newState;
      case actionTypes.FETCH_TENSORBOARDS_SUCCESS:
        newState.lastFetched = new LastFetchedNames();
        newState.lastFetched.count = action.count;
        for (const tensorboard of action.tensorboards) {
          newState = processBuild(tensorboard);
        }
        return newState;
      case actionTypes.GET_TENSORBOARD_SUCCESS:
        return processBuild(action.tensorboard);
      default:
        return state;
    }
  };
