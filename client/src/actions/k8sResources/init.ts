import { Action } from 'redux';

import { actionTypes } from './actionTypes';

export interface InitK8SResourceRequestAction extends Action {
  type: actionTypes.INIT_K8S_RESOURCE_REQUEST;
  name: string;
}

export function initK8SResourceRequestActionCreator(name: string): InitK8SResourceRequestAction {
  return {
    type: actionTypes.INIT_K8S_RESOURCE_REQUEST,
    name
  };
}

export type InitK8SResourceAction = InitK8SResourceRequestAction;

export function initK8SResourceState(resourceType: string, name: string, owner?: string): any {
  return (dispatch: any, getState: any) => {
    dispatch(initK8SResourceRequestActionCreator(name));
  };
}
