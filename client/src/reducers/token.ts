import * as Cookies from 'js-cookie';
import { Reducer } from 'redux';

import { actionTypes, TokenAction } from '../actions/token';
import { TokenEmptyState, TokenStateSchema } from '../models/token';

export const tokenReducer: Reducer<TokenStateSchema> =
  (state: TokenStateSchema = TokenEmptyState, action: TokenAction) => {

    switch (action.type) {
      case actionTypes.FETCH_TOKEN_SUCCESS:
        Cookies.set('token', action.token.token);
        Cookies.set('user', action.username);
        return {
          ...state,
          user: action.username,
          token: action.token.token,
          csrftoken: action.token.csrftoken
        };
      case actionTypes.DISCARD_TOKEN:
        Cookies.remove('token');
        Cookies.remove('user');
        Cookies.remove('sessionid');
        Cookies.remove('csrftoken');
        return {
          ...state,
          user: '',
          token: '',
          csrftoken: ''
        };
      default:
        return state;
    }
  };
