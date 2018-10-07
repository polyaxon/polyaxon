import { Action } from 'redux';

import { BASE_URL } from '../constants/api';
import { handleAuthError } from '../constants/utils';

export enum actionTypes {
  FETCH_HEALTH_STATUS = 'FETCH_HEALTH_STATUS',
  RECEIVE_HEALTH_STATUS = 'RECEIVE_HEALTH_STATUS',
}

export interface FetchHealthStatusAction extends Action {
  type: actionTypes.FETCH_HEALTH_STATUS;
}

export interface ReceiveHealthStatusAction extends Action {
  type: actionTypes.RECEIVE_HEALTH_STATUS;
  status: { [key: string]: any };
}

export type HealthStatusAction = FetchHealthStatusAction | ReceiveHealthStatusAction;

export function receiveHealthStatusActionCreator(status: { [key: string]: any }): ReceiveHealthStatusAction {
  return {
    type: actionTypes.RECEIVE_HEALTH_STATUS,
    status
  };
}

export function fetchHealthStatus(): any {
  return (dispatch: any) => {
    return fetch(BASE_URL + '/_status', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
    })
      .then((response) => handleAuthError(response, dispatch))
      .then((response) => response.json())
      .then((json) => dispatch(receiveHealthStatusActionCreator(json)));
  };
}
