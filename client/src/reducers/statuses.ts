import { Reducer } from 'redux';
import { normalize } from 'normalizr';

import * as _ from 'lodash';

import { StatusesAction, actionTypes } from '../actions/statuses';
import { StatusStateSchema, StatusEmptyState, StatusModel } from '../models/status';
import { StatusSchema } from '../constants/schemas';
import { LastFetchedIds } from '../models/utils';

export const StatusesReducer: Reducer<StatusStateSchema> =
  (state: StatusStateSchema = StatusEmptyState, action: StatusesAction) => {
    let newState = {...state};

    let processStatus = function (status: StatusModel) {
      let id = status.id;
      newState.lastFetched.ids.push(id);
      if (!_.includes(newState.ids, id)) {
        newState.ids.push(id);
      }
      let normalizedStatuses = normalize(status, StatusSchema).entities.statuses;
      newState.byIds[id] = {
        ...newState.byIds[id], ...normalizedStatuses[id]
      };
      return newState;
    };

    switch (action.type) {
      case actionTypes.REQUEST_STATUSES:
        newState.lastFetched = new LastFetchedIds();
        return newState;
      case actionTypes.RECEIVE_STATUSES:
        newState.lastFetched = new LastFetchedIds();
        newState.lastFetched.count = action.count;
        for (let build of action.statuses) {
          newState = processStatus(build);
        }
        return newState;
      default:
        return state;
    }
  };
