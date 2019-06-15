import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { AccessAction, actionTypes } from '../actions/access';
import { ACTIONS } from '../constants/actions';
import { AccessSchema } from '../constants/schemas';
import { AccessesEmptyState, AccessModel, AccessStateSchema } from '../models/access';
import {
  AlertEmptyState,
  AlertSchema,
  initErrorById,
  initErrorGlobal,
  processErrorById,
  processErrorGlobal
} from '../models/alerts';
import {
  initLoadingIndicator,
  initLoadingIndicatorById,
  LoadingIndicatorEmptyState,
  LoadingIndicatorSchema,
  processLoadingIndicatorById,
  processLoadingIndicatorGlobal
} from '../models/loadingIndicator';
import { LastFetchedNames } from '../models/utils';

export const AccessesReducer: Reducer<AccessStateSchema> =
  (state: AccessStateSchema = AccessesEmptyState, action: AccessAction) => {
    let newState = {...state};

    const processAccess = (access: AccessModel) => {
      const uniqueName = access.name;
      if (!_.includes(newState.lastFetched.names, uniqueName)) {
        newState.lastFetched.names.push(uniqueName);
      }
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      if (_.isNil(access.deleted)) {
        access.deleted = false;
      }
      const normalizedAccesses = normalize(access, AccessSchema).entities.accesses;
      newState.byUniqueNames[uniqueName] = {
        ...newState.byUniqueNames[uniqueName], ...normalizedAccesses[access.name]
      };
      return newState;
    };

    switch (action.type) {
      case actionTypes.DELETE_ACCESS_SUCCESS:
        return {
          ...state,
          uniqueNames: state.uniqueNames.filter(
            (name) => name !== action.name),
          lastFetched: {
            ...state.lastFetched,
            names: state.lastFetched.names.filter((name) => name !== action.name)
          },
        };
      case actionTypes.UPDATE_ACCESS_SUCCESS:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.name]: action.access}
        };
      case actionTypes.FETCH_ACCESSES_REQUEST:
        newState.lastFetched = new LastFetchedNames();
        return newState;
      case actionTypes.FETCH_ACCESSES_SUCCESS:
        newState.lastFetched = new LastFetchedNames();
        newState.lastFetched.count = action.count;
        for (const access of action.accesses) {
          newState = processAccess(access);
        }
        return newState;
      case actionTypes.GET_ACCESS_SUCCESS:
        newState = processAccess(action.access);
        newState.lastFetched.count += 1;
        return newState;
      default:
        return state;
    }
  };

export const LoadingIndicatorAccessReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: AccessAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_ACCESS_REQUEST:
        return {
          ...state,
          accesses: processLoadingIndicatorById(state.accesses, action.name, true, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_ACCESS_ERROR:
      case actionTypes.UPDATE_ACCESS_SUCCESS:
        return {
          ...state,
          accesses: processLoadingIndicatorById(state.accesses, action.name, false, ACTIONS.UPDATE)
        };

      case actionTypes.GET_ACCESS_REQUEST:
        return {
          ...state,
          accesses: processLoadingIndicatorGlobal(
            processLoadingIndicatorById(state.accesses, action.name, true, ACTIONS.GET),
            false,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_ACCESS_ERROR:
      case actionTypes.GET_ACCESS_SUCCESS:
        return {
          ...state,
          accesses: processLoadingIndicatorById(state.accesses, action.name, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_ACCESS_REQUEST:
        return {
          ...state,
          accesses: processLoadingIndicatorById(state.accesses, action.name, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_ACCESS_ERROR:
      case actionTypes.DELETE_ACCESS_SUCCESS:
        return {
          ...state,
          accesses: processLoadingIndicatorById(state.accesses, action.name, false, ACTIONS.DELETE)
        };

      case actionTypes.FETCH_ACCESSES_REQUEST:
        return {
          ...state,
          accesses: processLoadingIndicatorGlobal(state.accesses, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_ACCESSES_ERROR:
      case actionTypes.FETCH_ACCESSES_SUCCESS:
        return {
          ...state,
          accesses: processLoadingIndicatorGlobal(state.accesses, false, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_ACCESS_REQUEST:
        return {
          ...state,
          accesses: processLoadingIndicatorGlobal(state.accesses, true, ACTIONS.CREATE)
        };

      case actionTypes.CREATE_ACCESS_ERROR:
      case actionTypes.CREATE_ACCESS_SUCCESS:
        return {
          ...state,
          accesses: processLoadingIndicatorGlobal(state.accesses, false, ACTIONS.CREATE)
        };
      case actionTypes.INIT_ACCESS_REQUEST:
        return {
          ...state,
          accesses: action.name ?
            initLoadingIndicatorById(state.accesses, action.name) :
            initLoadingIndicator(state.accesses)
        };
      default:
        return state;
    }
  };

export const AlertAccessReducer: Reducer<AlertSchema> =
  (state: AlertSchema = AlertEmptyState, action: AccessAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_ACCESS_REQUEST:
        return {
          ...state,
          accesses: processErrorById(state.accesses, action.name, null, null, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_ACCESS_SUCCESS:
        return {
          ...state,
          accesses: processErrorById(state.accesses, action.name, null, true, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_ACCESS_ERROR:
        return {
          ...state,
          accesses: processErrorById(state.accesses, action.name, action.error, false, ACTIONS.UPDATE)
        };

      case actionTypes.GET_ACCESS_REQUEST:
        return {
          ...state,
          accesses: processErrorGlobal(
            processErrorById(state.accesses, action.name, null, null, ACTIONS.GET),
            null,
            null,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_ACCESS_SUCCESS:
        return {
          ...state,
          accesses: processErrorById(state.accesses, action.name, null, true, ACTIONS.GET)
        };
      case actionTypes.GET_ACCESS_ERROR:
        return {
          ...state,
          accesses: processErrorById(state.accesses, action.name, action.error, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_ACCESS_REQUEST:
        return {
          ...state,
          accesses: processErrorById(state.accesses, action.name, null, null, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_ACCESS_SUCCESS:
        return {
          ...state,
          accesses: processErrorById(state.accesses, action.name, null, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_ACCESS_ERROR:
        return {
          ...state,
          accesses: processErrorById(state.accesses, action.name, action.error, false, ACTIONS.DELETE)
        };

      case actionTypes.FETCH_ACCESSES_REQUEST:
        return {
          ...state,
          accesses: processErrorGlobal(state.accesses, null, null, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_ACCESSES_SUCCESS:
        return {
          ...state,
          accesses: processErrorGlobal(state.accesses, null, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_ACCESSES_ERROR:
        return {
          ...state,
          accesses: processErrorGlobal(state.accesses, action.error, false, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_ACCESS_REQUEST:
        return {
          ...state,
          accesses: processErrorGlobal(state.accesses, null, null, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_ACCESS_SUCCESS:
        return {
          ...state,
          accesses: processErrorGlobal(state.accesses, null, true, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_ACCESS_ERROR:
        return {
          ...state,
          accesses: processErrorGlobal(state.accesses, action.error, false, ACTIONS.CREATE)
        };

      case actionTypes.INIT_ACCESS_REQUEST:
        return {
          ...state,
          accesses: action.name ?
            initErrorById(state.accesses, action.name) :
            initErrorGlobal(state.accesses)
        };
      default:
        return state;
    }
  };
