import * as _ from 'lodash';
import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import { actionTypes, UserAction } from '../actions/user';
import { UserSchema } from '../constants/schemas';
import { UserEmptyState, UserModel, UserStateSchema } from '../models/user';

export const userReducer: Reducer<UserStateSchema> =
  (state: UserStateSchema = UserEmptyState, action: UserAction) => {
    const newState = {...state};

    const processUser = function(user: UserModel) {
      if (!_.includes(newState.userNames, user.username)) {
        newState.userNames.push(user.username);
      }
      const normalizedUsers = normalize(user, UserSchema).entities.users;
      newState.byUserNames[user.username] = {
        ...newState.byUserNames[user.username], ...normalizedUsers[user.username]
      };
      if (newState.byUserNames[user.username].projects == null) {
        newState.byUserNames[user.username].projects = [];
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.FETCH_USER_SUCCESS:
        return processUser(action.user);
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
