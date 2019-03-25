import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, ActivityLogAction } from '../actions/activityLog';
import { ACTIONS } from '../constants/actions';
import { activityLogSchema } from '../constants/schemas';
import { ActivityLogModel, ActivityLogsEmptyState, ActivityLogsStateSchema } from '../models/activitylog';
import { ErrorEmptyState, ErrorSchema, processErrorGlobal } from '../models/errors';
import {
  LoadingIndicatorEmptyState,
  LoadingIndicatorSchema,
  processLoadingIndicatorGlobal
} from '../models/loadingIndicator';
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
      case actionTypes.FETCH_ACTIVITY_LOGS_REQUEST:
        newState.lastFetched = new LastFetchedIds();
        return newState;
      case actionTypes.FETCH_ACTIVITY_LOGS_SUCCESS:
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

export const LoadingIndicatorActivityReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: ActivityLogAction) => {
    switch (action.type) {
      case actionTypes.FETCH_ACTIVITY_LOGS_REQUEST:
        return {
          ...state,
          activityLogs: processLoadingIndicatorGlobal(state.activityLogs, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_ACTIVITY_LOGS_ERROR:
      case actionTypes.FETCH_ACTIVITY_LOGS_SUCCESS:
        return {
          ...state,
          activityLogs: processLoadingIndicatorGlobal(state.activityLogs, false, ACTIONS.FETCH)
        };
      default:
        return state;
    }
  };

export const ErrorActivityReducer: Reducer<ErrorSchema> =
  (state: ErrorSchema = ErrorEmptyState, action: ActivityLogAction) => {
    switch (action.type) {
      case actionTypes.FETCH_ACTIVITY_LOGS_REQUEST:
      case actionTypes.FETCH_ACTIVITY_LOGS_SUCCESS:
        return {
          ...state,
          activityLogs: processErrorGlobal(state.activityLogs, null, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_ACTIVITY_LOGS_ERROR:
        return {
          ...state,
          activityLogs: processErrorGlobal(state.activityLogs, action.error, ACTIONS.FETCH)
        };
      default:
        return state;
    }
  };
