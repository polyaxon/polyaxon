import { Reducer } from 'redux';
import { normalize } from 'normalizr';
import * as _ from 'lodash';

import { UserAction, actionTypes } from '../actions/user';
import { UserStateSchema, UserEmptyState, UserModel } from '../models/user';
import { UserSchema } from '../constants/schemas';

export const userReducer: Reducer<UserStateSchema> =
  (state: UserStateSchema = UserEmptyState, action: UserAction) => {
    let newState = {...state};

    let processUser = function (user: UserModel) {
      if (!_.includes(newState.userNames, user.username)) {
        newState.userNames.push(user.username);
      }
      let normalizedUsers = normalize(user, UserSchema).entities.users;
      newState.byUserNames[user.username] = {
        ...newState.byUserNames[user.username], ...normalizedUsers[user.username]
      };
      if (newState.byUserNames[user.username].projects == null) {
        newState.byUserNames[user.username].projects = [];
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.RECEIVE_USER:
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
