import { Reducer } from 'redux';
import * as Cookies from 'js-cookie';

import { TokenAction, actionTypes } from '../actions/token';
import { TokenStateSchema, TokenEmptyState } from '../models/token';

export const tokenReducer: Reducer<TokenStateSchema> =
  (state: TokenStateSchema = TokenEmptyState, action: TokenAction) => {

    switch (action.type) {
      case actionTypes.RECEIVE_TOKEN:
        // Cookies.set('token', action.token.token);
        // Cookies.set('user', action.username);
        return {
          ...state,
          user: action.username,
          token: action.token.token
        };
      case actionTypes.DISCARD_TOKEN:
        // Cookies.remove('token');
        // Cookies.remove('user');
        // Cookies.remove('sessionid');
        return {
          ...state,
          user: '',
          token: ''
        };
      default:
        return state;
    }
  };
