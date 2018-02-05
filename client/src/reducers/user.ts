import { Reducer } from 'redux';

import { UserAction, actionTypes } from '../actions/user';
import { UserModel, UserEmptyState } from '../models/user';

export const userReducer: Reducer<UserModel> =
  (state: UserModel = UserEmptyState, action: UserAction) => {
    switch (action.type) {
      case actionTypes.RECEIVE_USER:
        return {
          ...state,
          username: action.user.username,
          email: action.user.email,
          isSuperuser: action.user.isSuperuser
        };
      case actionTypes.DISCARD_USER:
        return {
          ...state,
          username: '',
          email: '',
          isSuperuser: false,
        };
      default:
        return state;
    }
  };
