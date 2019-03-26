import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, TensorboardAction } from '../actions/tensorboards';
import { ACTIONS } from '../constants/actions';
import { TensorboardSchema } from '../constants/schemas';
import { STOPPED } from '../constants/statuses';
import { AlertEmptyState, AlertSchema, processErrorById, processErrorGlobal } from '../models/alerts';
import {
  LoadingIndicatorEmptyState,
  LoadingIndicatorSchema,
  processLoadingIndicatorById,
  processLoadingIndicatorGlobal
} from '../models/loadingIndicator';
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

export const LoadingIndicatorTensorboardsReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: TensorboardAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_TENSORBOARD_REQUEST:
        return {
          ...state,
          tensorboards: processLoadingIndicatorById(state.tensorboards, action.tensorboardName, true, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_TENSORBOARD_ERROR:
      case actionTypes.UPDATE_TENSORBOARD_SUCCESS:
        return {
          ...state,
          tensorboards: processLoadingIndicatorById(state.tensorboards, action.tensorboardName, false, ACTIONS.UPDATE)
        };

      case actionTypes.GET_TENSORBOARD_REQUEST:
        return {
          ...state,
          tensorboards: processLoadingIndicatorGlobal(
            processLoadingIndicatorById(state.tensorboards, action.tensorboardName, true, ACTIONS.GET),
            false,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_TENSORBOARD_ERROR:
      case actionTypes.GET_TENSORBOARD_SUCCESS:
        return {
          ...state,
          tensorboards: processLoadingIndicatorById(state.tensorboards, action.tensorboardName, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_TENSORBOARD_REQUEST:
        return {
          ...state,
          tensorboards: processLoadingIndicatorById(state.tensorboards, action.tensorboardName, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_TENSORBOARD_ERROR:
      case actionTypes.DELETE_TENSORBOARD_SUCCESS:
        return {
          ...state,
          tensorboards: processLoadingIndicatorById(state.tensorboards, action.tensorboardName, false, ACTIONS.DELETE)
        };

      case actionTypes.ARCHIVE_TENSORBOARD_REQUEST:
        return {
          ...state,
          tensorboards: processLoadingIndicatorById(state.tensorboards, action.tensorboardName, true, ACTIONS.ARCHIVE)
        };
      case actionTypes.ARCHIVE_TENSORBOARD_ERROR:
      case actionTypes.ARCHIVE_TENSORBOARD_SUCCESS:
        return {
          ...state,
          tensorboards: processLoadingIndicatorById(state.tensorboards, action.tensorboardName, false, ACTIONS.ARCHIVE)
        };

      case actionTypes.RESTORE_TENSORBOARD_REQUEST:
        return {
          ...state,
          tensorboards: processLoadingIndicatorById(state.tensorboards, action.tensorboardName, true, ACTIONS.RESTORE)
        };
      case actionTypes.RESTORE_TENSORBOARD_ERROR:
      case actionTypes.RESTORE_TENSORBOARD_SUCCESS:
        return {
          ...state,
          tensorboards: processLoadingIndicatorById(state.tensorboards, action.tensorboardName, false, ACTIONS.RESTORE)
        };

      case actionTypes.STOP_TENSORBOARD_REQUEST:
        return {
          ...state,
          tensorboards: processLoadingIndicatorById(state.tensorboards, action.tensorboardName, true, ACTIONS.STOP)
        };
      case actionTypes.STOP_TENSORBOARD_ERROR:
      case actionTypes.STOP_TENSORBOARD_SUCCESS:
        return {
          ...state,
          tensorboards: processLoadingIndicatorById(state.tensorboards,
                                                    action.tensorboardName,
                                                    false,
                                                    ACTIONS.STOP)
        };

      case actionTypes.BOOKMARK_TENSORBOARD_REQUEST:
        return {
          ...state,
          tensorboards: processLoadingIndicatorById(state.tensorboards,
                                                    action.tensorboardName,
                                                    true,
                                                    ACTIONS.BOOKMARK)
        };
      case actionTypes.BOOKMARK_TENSORBOARD_ERROR:
      case actionTypes.BOOKMARK_TENSORBOARD_SUCCESS:
        return {
          ...state,
          tensorboards: processLoadingIndicatorById(state.tensorboards,
                                                    action.tensorboardName,
                                                    false,
                                                    ACTIONS.BOOKMARK)
        };

      case actionTypes.UNBOOKMARK_TENSORBOARD_REQUEST:
        return {
          ...state,
          tensorboards: processLoadingIndicatorById(
            state.tensorboards,
            action.tensorboardName,
            true,
            ACTIONS.UNBOOKMARK)
        };
      case actionTypes.UNBOOKMARK_TENSORBOARD_ERROR:
      case actionTypes.UNBOOKMARK_TENSORBOARD_SUCCESS:
        return {
          ...state,
          tensorboards: processLoadingIndicatorById(state.tensorboards,
                                                    action.tensorboardName,
                                                    false,
                                                    ACTIONS.UNBOOKMARK)
        };

      case actionTypes.FETCH_TENSORBOARDS_REQUEST:
        return {
          ...state,
          tensorboards: processLoadingIndicatorGlobal(state.tensorboards, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_TENSORBOARDS_ERROR:
      case actionTypes.FETCH_TENSORBOARDS_SUCCESS:
        return {
          ...state,
          tensorboards: processLoadingIndicatorGlobal(state.tensorboards, false, ACTIONS.FETCH)
        };
      default:
        return state;
    }
  };

export const AlertTensorboardsReducer: Reducer<AlertSchema> =
  (state: AlertSchema = AlertEmptyState, action: TensorboardAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_TENSORBOARD_REQUEST:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards, action.tensorboardName, null, null, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_TENSORBOARD_SUCCESS:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards, action.tensorboardName, null, true, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_TENSORBOARD_ERROR:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards,
                                         action.tensorboardName,
                                         action.error,
                                         false,
                                         ACTIONS.UPDATE)
        };

      case actionTypes.GET_TENSORBOARD_REQUEST:
        return {
          ...state,
          tensorboards: processErrorGlobal(
            processErrorById(state.tensorboards, action.tensorboardName, null, null, ACTIONS.GET),
            null,
            null,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_TENSORBOARD_SUCCESS:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards, action.tensorboardName, null, null, ACTIONS.GET)
        };
      case actionTypes.GET_TENSORBOARD_ERROR:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards, action.tensorboardName, action.error, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_TENSORBOARD_REQUEST:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards, action.tensorboardName, null, null, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_TENSORBOARD_SUCCESS:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards, action.tensorboardName, null, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_TENSORBOARD_ERROR:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards,
                                         action.tensorboardName,
                                         action.error,
                                         false,
                                         ACTIONS.DELETE)
        };

      case actionTypes.ARCHIVE_TENSORBOARD_REQUEST:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards, action.tensorboardName, null, null, ACTIONS.ARCHIVE)
        };
      case actionTypes.ARCHIVE_TENSORBOARD_SUCCESS:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards, action.tensorboardName, null, true, ACTIONS.ARCHIVE)
        };
      case actionTypes.ARCHIVE_TENSORBOARD_ERROR:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards,
                                         action.tensorboardName,
                                         action.error,
                                         false,
                                         ACTIONS.ARCHIVE)
        };

      case actionTypes.RESTORE_TENSORBOARD_REQUEST:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards, action.tensorboardName, null, null, ACTIONS.RESTORE)
        };
      case actionTypes.RESTORE_TENSORBOARD_SUCCESS:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards, action.tensorboardName, null, true, ACTIONS.RESTORE)
        };
      case actionTypes.RESTORE_TENSORBOARD_ERROR:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards,
                                         action.tensorboardName,
                                         action.error,
                                         false,
                                         ACTIONS.RESTORE)
        };

      case actionTypes.STOP_TENSORBOARD_REQUEST:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards, action.tensorboardName, null, null, ACTIONS.STOP)
        };
      case actionTypes.STOP_TENSORBOARD_SUCCESS:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards, action.tensorboardName, null, true, ACTIONS.STOP)
        };
      case actionTypes.STOP_TENSORBOARD_ERROR:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards,
                                         action.tensorboardName,
                                         action.error,
                                         false,
                                         ACTIONS.STOP)
        };

      case actionTypes.BOOKMARK_TENSORBOARD_REQUEST:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards,
                                         action.tensorboardName,
                                         null,
                                         null,
                                         ACTIONS.BOOKMARK)
        };
      case actionTypes.BOOKMARK_TENSORBOARD_SUCCESS:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards,
                                         action.tensorboardName,
                                         null,
                                         true,
                                         ACTIONS.BOOKMARK)
        };
      case actionTypes.BOOKMARK_TENSORBOARD_ERROR:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards,
                                         action.tensorboardName,
                                         action.error,
                                         false,
                                         ACTIONS.BOOKMARK)
        };

      case actionTypes.UNBOOKMARK_TENSORBOARD_REQUEST:
        return {
          ...state,
          tensorboards: processErrorById(
            state.tensorboards,
            action.tensorboardName,
            null,
            null,
            ACTIONS.UNBOOKMARK)
        };
      case actionTypes.UNBOOKMARK_TENSORBOARD_SUCCESS:
        return {
          ...state,
          tensorboards: processErrorById(
            state.tensorboards,
            action.tensorboardName,
            null,
            true,
            ACTIONS.UNBOOKMARK)
        };
      case actionTypes.UNBOOKMARK_TENSORBOARD_ERROR:
        return {
          ...state,
          tensorboards: processErrorById(state.tensorboards,
                                         action.tensorboardName,
                                         action.error,
                                         false,
                                         ACTIONS.UNBOOKMARK)
        };

      case actionTypes.FETCH_TENSORBOARDS_REQUEST:
        return {
          ...state,
          tensorboards: processErrorGlobal(state.tensorboards, null, null, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_TENSORBOARDS_SUCCESS:
        return {
          ...state,
          tensorboards: processErrorGlobal(state.tensorboards, null, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_TENSORBOARDS_ERROR:
        return {
          ...state,
          tensorboards: processErrorGlobal(state.tensorboards, action.error, false, ACTIONS.FETCH)
        };
      default:
        return state;
    }
  };
