import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, SearchAction } from '../actions/search';
import { searchSchema } from '../constants/schemas';
import {
  SearchesEmptyState,
  SearchesStateSchema,
  SearchModel
} from '../models/search';
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
      case actionTypes.GET_SEARCH_SUCCESS_SUCCESS:
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
