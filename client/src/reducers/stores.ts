import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, StoreAction } from '../actions/stores';
import { ACTIONS } from '../constants/actions';
import { StoreSchema } from '../constants/schemas';
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
import { StoreModel, StoresEmptyState, StoreStateSchema } from '../models/store';
import { LastFetchedNames } from '../models/utils';

export const StoresReducer: Reducer<StoreStateSchema> =
  (state: StoreStateSchema = StoresEmptyState, action: StoreAction) => {
    let newState = {...state};

    const processStore = (store: StoreModel) => {
      const uniqueName = store.name;
      if (!_.includes(newState.lastFetched.names, uniqueName)) {
        newState.lastFetched.names.push(uniqueName);
      }
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      if (_.isNil(store.deleted)) {
        store.deleted = false;
      }
      const normalizedStores = normalize(store, StoreSchema).entities.stores;
      newState.byUniqueNames[uniqueName] = {
        ...newState.byUniqueNames[uniqueName], ...normalizedStores[store.name]
      };
      return newState;
    };

    switch (action.type) {
      case actionTypes.DELETE_STORE_SUCCESS:
        return {
          ...state,
          uniqueNames: state.uniqueNames.filter(
            (name) => name !== action.name),
          lastFetched: {
            ...state.lastFetched,
            names: state.lastFetched.names.filter((name) => name !== action.name)
          },
        };
      case actionTypes.UPDATE_STORE_SUCCESS:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.name]: action.store}
        };
      case actionTypes.FETCH_STORES_REQUEST:
        newState.lastFetched = new LastFetchedNames();
        return newState;
      case actionTypes.FETCH_STORES_SUCCESS:
        newState.lastFetched = new LastFetchedNames();
        newState.lastFetched.count = action.count;
        for (const store of action.stores) {
          newState = processStore(store);
        }
        return newState;
      case actionTypes.GET_STORE_SUCCESS:
        newState = processStore(action.store);
        newState.lastFetched.count += 1;
        return newState;
      default:
        return state;
    }
  };

export const LoadingIndicatorStoreReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: StoreAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_STORE_REQUEST:
        return {
          ...state,
          stores: processLoadingIndicatorById(state.stores, action.name, true, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_STORE_ERROR:
      case actionTypes.UPDATE_STORE_SUCCESS:
        return {
          ...state,
          stores: processLoadingIndicatorById(state.stores, action.name, false, ACTIONS.UPDATE)
        };

      case actionTypes.GET_STORE_REQUEST:
        return {
          ...state,
          stores: processLoadingIndicatorGlobal(
            processLoadingIndicatorById(state.stores, action.name, true, ACTIONS.GET),
            false,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_STORE_ERROR:
      case actionTypes.GET_STORE_SUCCESS:
        return {
          ...state,
          stores: processLoadingIndicatorById(state.stores, action.name, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_STORE_REQUEST:
        return {
          ...state,
          stores: processLoadingIndicatorById(state.stores, action.name, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_STORE_ERROR:
      case actionTypes.DELETE_STORE_SUCCESS:
        return {
          ...state,
          stores: processLoadingIndicatorById(state.stores, action.name, false, ACTIONS.DELETE)
        };

      case actionTypes.FETCH_STORES_REQUEST:
        return {
          ...state,
          stores: processLoadingIndicatorGlobal(state.stores, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_STORES_ERROR:
      case actionTypes.FETCH_STORES_SUCCESS:
        return {
          ...state,
          stores: processLoadingIndicatorGlobal(state.stores, false, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_STORE_REQUEST:
        return {
          ...state,
          stores: processLoadingIndicatorGlobal(state.stores, true, ACTIONS.CREATE)
        };

      case actionTypes.CREATE_STORE_ERROR:
      case actionTypes.CREATE_STORE_SUCCESS:
        return {
          ...state,
          stores: processLoadingIndicatorGlobal(state.stores, false, ACTIONS.CREATE)
        };
      case actionTypes.INIT_STORE_REQUEST:
        return {
          ...state,
          stores: action.name ?
            initLoadingIndicatorById(state.stores, action.name) :
            initLoadingIndicator(state.stores)
        };
      default:
        return state;
    }
  };

export const AlertStoreReducer: Reducer<AlertSchema> =
  (state: AlertSchema = AlertEmptyState, action: StoreAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_STORE_REQUEST:
        return {
          ...state,
          stores: processErrorById(state.stores, action.name, null, null, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_STORE_SUCCESS:
        return {
          ...state,
          stores: processErrorById(state.stores, action.name, null, true, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_STORE_ERROR:
        return {
          ...state,
          stores: processErrorById(state.stores, action.name, action.error, false, ACTIONS.UPDATE)
        };

      case actionTypes.GET_STORE_REQUEST:
        return {
          ...state,
          stores: processErrorGlobal(
            processErrorById(state.stores, action.name, null, null, ACTIONS.GET),
            null,
            null,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_STORE_SUCCESS:
        return {
          ...state,
          stores: processErrorById(state.stores, action.name, null, true, ACTIONS.GET)
        };
      case actionTypes.GET_STORE_ERROR:
        return {
          ...state,
          stores: processErrorById(state.stores, action.name, action.error, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_STORE_REQUEST:
        return {
          ...state,
          stores: processErrorById(state.stores, action.name, null, null, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_STORE_SUCCESS:
        return {
          ...state,
          stores: processErrorById(state.stores, action.name, null, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_STORE_ERROR:
        return {
          ...state,
          stores: processErrorById(state.stores, action.name, action.error, false, ACTIONS.DELETE)
        };

      case actionTypes.FETCH_STORES_REQUEST:
        return {
          ...state,
          stores: processErrorGlobal(state.stores, null, null, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_STORES_SUCCESS:
        return {
          ...state,
          stores: processErrorGlobal(state.stores, null, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_STORES_ERROR:
        return {
          ...state,
          stores: processErrorGlobal(state.stores, action.error, false, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_STORE_REQUEST:
        return {
          ...state,
          stores: processErrorGlobal(state.stores, null, null, ACTIONS.CREATE)
        };
        case actionTypes.CREATE_STORE_SUCCESS:
        return {
          ...state,
          stores: processErrorGlobal(state.stores, null, true, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_STORE_ERROR:
        return {
          ...state,
          stores: processErrorGlobal(state.stores, action.error, false, ACTIONS.CREATE)
        };

      case actionTypes.INIT_STORE_REQUEST:
        return {
          ...state,
          stores: action.name ?
            initErrorById(state.stores, action.name) :
            initErrorGlobal(state.stores)
        };
      default:
        return state;
    }
  };
