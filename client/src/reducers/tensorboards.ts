import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, TensorboardAction } from '../actions/tensorboard';
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
      case actionTypes.CREATE_TENSORBOARD:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.tensorboard.unique_name]: action.tensorboard},
          uniqueNames: [...state.uniqueNames, action.tensorboard.unique_name]
        };
      case actionTypes.DELETE_TENSORBOARD:
        return {
          ...state,
          uniqueNames: state.uniqueNames.filter(
            (name) => name !== action.tensorboardName),
          lastFetched: {
            ...state.lastFetched,
            names: state.lastFetched.names.filter((name) => name !== action.tensorboardName)
          },
        };
      case actionTypes.ARCHIVE_TENSORBOARD:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.tensorboardName]: {
              ...state.byUniqueNames[action.tensorboardName], deleted: true
            }
          },
        };
      case actionTypes.RESTORE_TENSORBOARD:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.tensorboardName]: {
              ...state.byUniqueNames[action.tensorboardName], deleted: false
            }
          },
        };
      case actionTypes.STOP_TENSORBOARD:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.tensorboardName]: {
              ...state.byUniqueNames[action.tensorboardName], last_status: STOPPED
            }
          },
        };
      case actionTypes.BOOKMARK_TENSORBOARD:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.tensorboardName]: {
              ...state.byUniqueNames[action.tensorboardName], bookmarked: true
            }
          },
        };
      case actionTypes.UNBOOKMARK_TENSORBOARD:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.tensorboardName]: {
              ...state.byUniqueNames[action.tensorboardName], bookmarked: false
            }
          },
        };
      case actionTypes.UPDATE_TENSORBOARD:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.tensorboard.unique_name]: action.tensorboard}
        };
      case actionTypes.REQUEST_TENSORBOARDS:
        newState.lastFetched = new LastFetchedNames();
        return newState;
      case actionTypes.RECEIVE_TENSORBOARDS:
        newState.lastFetched = new LastFetchedNames();
        newState.lastFetched.count = action.count;
        for (const tensorboard of action.tensorboards) {
          newState = processBuild(tensorboard);
        }
        return newState;
      case actionTypes.RECEIVE_TENSORBOARD:
        return processBuild(action.tensorboard);
      default:
        return state;
    }
  };
