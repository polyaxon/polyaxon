import { Reducer } from 'redux';
import { actionTypes, LogsAction } from '../actions/logs';

export const logsReducer: Reducer<string> =
  (state: string = '', action: LogsAction) => {
    switch (action.type) {

      case actionTypes.FETCH_LOGS_REQUEST:
        return 'Fetching logs...';
      case actionTypes.FETCH_LOGS_SUCCESS:
        return action.logs;
      case actionTypes.FETCH_LOGS_ERROR:
        return action.error;
      default:
        return state;
    }
  };
