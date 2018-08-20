import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, ActivityLogAction } from '../actions/activityLog';
import { activityLogSchema } from '../constants/schemas';
import {
  ActivityLogModel,
  ActivityLogsEmptyState,
  ActivityLogsStateSchema
} from '../models/activitylog';
import { LastFetchedIds } from '../models/utils';

export const activityLogsReducer: Reducer<ActivityLogsStateSchema> =
  (state: ActivityLogsStateSchema = ActivityLogsEmptyState, action: ActivityLogAction) => {
    let newState = {...state};

    const processActivityLog = (activityLog: ActivityLogModel) => {
      newState.lastFetched.ids.push(activityLog.id);
      if (!_.includes(newState.ids, activityLog.id)) {
        newState.ids.push(activityLog.id);
      }
      const normalizedBuilds = normalize(activityLog, activityLogSchema).entities.activityLogs;
      newState.byIds[activityLog.id] = {
        ...newState.byIds[activityLog.id], ...normalizedBuilds[activityLog.id]
      };
      return newState;
    };

    switch (action.type) {
      case actionTypes.REQUEST_ACTIVITY_LOGS:
        newState.lastFetched = new LastFetchedIds();
        return newState;
      case actionTypes.RECEIVE_ACTIVITY_LOGS:
        newState.lastFetched = new LastFetchedIds();
        newState.lastFetched.count = action.count;
        for (const build of action.activityLogs) {
          newState = processActivityLog(build);
        }
        return newState;
      default:
        return state;
    }
  };
