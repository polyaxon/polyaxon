import {Reducer} from "redux";

import {TokenAction, actionTypes} from "../actions/token";
import {TokenStateSchema, TokenEmptyState} from "../models/token";

export const tokenReducer: Reducer<TokenStateSchema> =
	(state: TokenStateSchema = TokenEmptyState, action: TokenAction) => {

  switch(action.type){
    case actionTypes.RECEIVE_TOKEN:
      return {
        ...state,
        user: action.username,
        token: action.token.token
      };
    case actionTypes.DISCARD_TOKEN:
      return {
        ...state,
        user: '',
        token: ''
      };
    default:
      return state;
  }
}
