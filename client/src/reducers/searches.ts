import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, SearchAction } from '../actions/search';
import { ACTIONS } from '../constants/actions';
import { searchSchema } from '../constants/schemas';
import { AlertEmptyState, AlertSchema, processErrorById, processErrorGlobal } from '../models/alerts';
import {
  LoadingIndicatorEmptyState,
  LoadingIndicatorSchema,
  processLoadingIndicatorById,
  processLoadingIndicatorGlobal
} from '../models/loadingIndicator';
import { SearchesEmptyState, SearchesStateSchema, SearchModel } from '../models/search';
import { LastFetchedIds } from '../models/utils';

export const searchesReducer: Reducer<SearchesStateSchema> =
  (state: SearchesStateSchema = SearchesEmptyState, action: SearchAction) => {
    let newState = {...state};

    const processSearch = (search: SearchModel) => {
      newState.lastFetched.ids.push(search.id);
      if (!_.includes(newState.ids, search.id)) {
        newState.ids.push(search.id);
      }
      const normalizedBuilds = normalize(search, searchSchema).entities.searches;
      newState.byIds[search.id] = {
        ...newState.byIds[search.id], ...normalizedBuilds[search.id]
      };
      return newState;
    };

    switch (action.type) {
      case actionTypes.FETCH_SEARCHES_REQUEST:
        newState.lastFetched = new LastFetchedIds();
        return newState;
      case actionTypes.GET_SEARCH_SUCCESS:
        return processSearch(action.search);
      case actionTypes.DELETE_SEARCH_SUCCESS:
        return {
          ...state,
          ids: state.ids.filter(
            (id) => id !== action.searchId),
          lastFetched: {
            ...state.lastFetched,
            ids: state.lastFetched.ids.filter(
              (id) => id !== action.searchId)
          },
        };
      case actionTypes.FETCH_SEARCHES_SUCCESS:
        newState.lastFetched = new LastFetchedIds();
        newState.lastFetched.count = action.count;
        for (const search of action.searches) {
          newState = processSearch(search);
        }
        return newState;
      default:
        return state;
    }
  };

export const LoadingIndicatorSearchesReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: SearchAction) => {
    switch (action.type) {
      case actionTypes.GET_SEARCH_SUCCESS:
        return {
          ...state,
          searches: processLoadingIndicatorById(state.searches, action.searchId, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_SEARCH_REQUEST:
        return {
          ...state,
          searches: processLoadingIndicatorById(state.searches, action.searchId, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_SEARCH_ERROR:
      case actionTypes.DELETE_SEARCH_SUCCESS:
        return {
          ...state,
          searches: processLoadingIndicatorById(state.searches, action.searchId, false, ACTIONS.DELETE)
        };

      case actionTypes.FETCH_SEARCHES_REQUEST:
        return {
          ...state,
          searches: processLoadingIndicatorGlobal(state.searches, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_SEARCHES_ERROR:
      case actionTypes.FETCH_SEARCHES_SUCCESS:
        return {
          ...state,
          searches: processLoadingIndicatorGlobal(state.searches, false, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_SEARCH_REQUEST:
        return {
          ...state,
          searches: processLoadingIndicatorGlobal(state.searches, true, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_SEARCH_ERROR:
        return {
          ...state,
          searches: processLoadingIndicatorGlobal(state.searches, false, ACTIONS.CREATE)
        };
      default:
        return state;
    }
  };

export const AlertSearchesReducer: Reducer<AlertSchema> =
  (state: AlertSchema = AlertEmptyState, action: SearchAction) => {
    switch (action.type) {
      case actionTypes.GET_SEARCH_SUCCESS:
        return {
          ...state,
          searches: processErrorById(state.searches, action.searchId, null, true, ACTIONS.GET)
        };

      case actionTypes.DELETE_SEARCH_REQUEST:
        return {
          ...state,
          searches: processErrorById(state.searches, action.searchId, null, null, ACTIONS.GET)
        };
      case actionTypes.DELETE_SEARCH_SUCCESS:
        return {
          ...state,
          searches: processErrorById(state.searches, action.searchId, null, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_SEARCH_ERROR:
        return {
          ...state,
          searches: processErrorById(state.searches, action.searchId, action.error, false, ACTIONS.DELETE)
        };

      case actionTypes.FETCH_SEARCHES_REQUEST:
        return {
          ...state,
          searches: processErrorGlobal(state.searches, null, null, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_SEARCHES_SUCCESS:
        return {
          ...state,
          searches: processErrorGlobal(state.searches, null, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_SEARCHES_ERROR:
        return {
          ...state,
          searches: processErrorGlobal(state.searches, action.error, false, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_SEARCH_REQUEST:
        return {
          ...state,
          searches: processErrorGlobal(state.searches, null, null, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_SEARCH_SUCCESS:
        return {
          ...state,
          searches: processErrorGlobal(state.searches, null, true, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_SEARCH_ERROR:
        return {
          ...state,
          searches: processErrorGlobal(state.searches, action.error, false, ACTIONS.CREATE)
        };
      default:
        return state;
    }
  };
