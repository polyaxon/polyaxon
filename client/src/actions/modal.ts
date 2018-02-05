import { Action } from 'redux';

import { ModalStateSchema } from '../models/modal';

export enum actionTypes {
  SHOW_MODAL = 'SHOW_MODAL',
  HIDE_MODAL = 'HIDE_MODAL'
}

export interface ModalAction extends Action {
  type: actionTypes.SHOW_MODAL | actionTypes.HIDE_MODAL;
  modalProps: ModalStateSchema;
}

export function showModal(modalProps: ModalStateSchema): ModalAction {
  return {
    type: actionTypes.SHOW_MODAL,
    modalProps
  };
}

export function hideModal(modalProps: ModalStateSchema): ModalAction {
  return {
    type: actionTypes.HIDE_MODAL,
    modalProps
  };
}
