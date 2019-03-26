import { Reducer } from 'redux';

import { actionTypes, HealthStatusAction } from '../actions/healthStatus';
import { ACTIONS } from '../constants/actions';
import { AlertEmptyState, AlertSchema, processErrorGlobal } from '../models/alerts';
import { HealthStatusEmptyState, HealthStatusStateSchema } from '../models/healthStatus';
import {
  LoadingIndicatorEmptyState,
  LoadingIndicatorSchema,
  processLoadingIndicatorGlobal
} from '../models/loadingIndicator';

export const HealthStatusReducer: Reducer<HealthStatusStateSchema> =
  (state: HealthStatusStateSchema = HealthStatusEmptyState, action: HealthStatusAction) => {

    switch (action.type) {
      case actionTypes.FETCH_HEALTH_STATUS_SUCCESS:
        return {
          ...state,
          status: action.status,
        };
      default:
        return state;
    }
  };

export const LoadingIndicatorHealthStatusReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: HealthStatusAction) => {
    switch (action.type) {
      case actionTypes.FETCH_HEALTH_STATUS_REQUEST:
        return {
          ...state,
          healthStatus: processLoadingIndicatorGlobal(state.healthStatus, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_HEALTH_STATUS_ERROR:
      case actionTypes.FETCH_HEALTH_STATUS_SUCCESS:
        return {
          ...state,
          healthStatus: processLoadingIndicatorGlobal(state.healthStatus, false, ACTIONS.FETCH)
        };
      default:
        return state;
    }
  };

export const AlertHealthStatusReducer: Reducer<AlertSchema> =
  (state: AlertSchema = AlertEmptyState, action: HealthStatusAction) => {
    switch (action.type) {
      case actionTypes.FETCH_HEALTH_STATUS_REQUEST:
        return {
          ...state,
          healthStatus: processErrorGlobal(state.healthStatus, null, null, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_HEALTH_STATUS_SUCCESS:
        return {
          ...state,
          healthStatus: processErrorGlobal(state.healthStatus, null, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_HEALTH_STATUS_ERROR:
        return {
          ...state,
          healthStatus: processErrorGlobal(state.healthStatus, action.error, false, ACTIONS.FETCH)
        };
      default:
        return state;
    }
  };
