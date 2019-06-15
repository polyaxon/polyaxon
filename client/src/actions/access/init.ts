import { Action } from 'redux';

import { actionTypes } from './actionTypes';

export interface InitAccessRequestAction extends Action {
  type: actionTypes.INIT_ACCESS_REQUEST;
  name: string;
}

export function initAccessRequestActionCreator(name: string): InitAccessRequestAction {
  return {
    type: actionTypes.INIT_ACCESS_REQUEST,
    name
  };
}

export type InitAccessAction = InitAccessRequestAction;

export function initAccessState(resourceType: string, name: string, owner?: string): any {
  return (dispatch: any, getState: any) => {
    dispatch(initAccessRequestActionCreator(name));
  };
}
