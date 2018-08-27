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
      case actionTypes.REQUEST_SEARCHES:
        newState.lastFetched = new LastFetchedIds();
        return newState;
      case actionTypes.RECEIVE_SEARCHES:
        newState.lastFetched = new LastFetchedIds();
        newState.lastFetched.count = action.count;
        for (const build of action.searches) {
          newState = processSearch(build);
        }
        return newState;
      default:
        return state;
    }
  };
