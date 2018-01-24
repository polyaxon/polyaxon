import {Reducer} from "redux";

import {ModalAction, actionTypes} from "../actions/modal";
import {ModalEmptyState, ModalStateSchema} from "../models/modal";


export const modalReducer: Reducer<ModalStateSchema> =
  (state: ModalStateSchema = ModalEmptyState, action: ModalAction) => {

    switch (action.type) {
      case actionTypes.SHOW_MODAL:
        return action.modalProps;
      case actionTypes.HIDE_MODAL:
        return action.modalProps;
      default:
        return state
    }
  };
