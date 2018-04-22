import { Reducer } from 'redux';
import { LogsAction, actionTypes } from '../actions/logs';

export const logsReducer: Reducer<string> =
  (state: string = '', action: LogsAction) => {
    switch (action.type) {

      case actionTypes.REQUEST_LOGS:
        return '';
      case actionTypes.RECEIVE_LOGS:
        return action.logs;
      default:
        return state;
    }
  };
