import { Reducer } from 'redux';

import { actionTypes, HealthStatusAction } from '../actions/healthStatus';
import { HealthStatusEmptyState, HealthStatusStateSchema } from '../models/healthStatus';

export const healthStatusReducer: Reducer<HealthStatusStateSchema> =
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
