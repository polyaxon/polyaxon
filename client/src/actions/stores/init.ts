import { Action } from 'redux';

import { actionTypes } from './actionTypes';

export interface InitStoreRequestAction extends Action {
  type: actionTypes.INIT_STORE_REQUEST;
  name: string;
}

export function initStoreRequestActionCreator(name: string): InitStoreRequestAction {
  return {
    type: actionTypes.INIT_STORE_REQUEST,
    name
  };
}

export type InitStoreAction = InitStoreRequestAction;

export function initStoreState(resourceType: string, name: string, owner?: string): any {
  return (dispatch: any, getState: any) => {
    dispatch(initStoreRequestActionCreator(name));
  };
}
