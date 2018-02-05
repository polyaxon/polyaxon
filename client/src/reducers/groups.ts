import {Reducer} from "redux";
import * as _ from "lodash";
import {normalize} from 'normalizr';

import {GroupSchema} from "../constants/schemas"
import {GroupAction, actionTypes} from "../actions/group";
import {GroupStateSchema, GroupsEmptyState} from "../models/group";

export const groupsReducer: Reducer<GroupStateSchema> =
  (state: GroupStateSchema = GroupsEmptyState, action: GroupAction) => {

    switch (action.type) {
      case actionTypes.CREATE_GROUP:
        return {
          ...state,
          ByUniqueNames: {...state.ByUniqueNames, [action.group.unique_name]: action.group},
          uniqueNames: [...state.uniqueNames, action.group.unique_name]
        };
      case actionTypes.DELETE_GROUP:
        return {
          ...state,
          ByUniqueNames: {
            ...state.ByUniqueNames,
            [action.group.unique_name]: {
              ...state.ByUniqueNames[action.group.unique_name], deleted: true}
          },
          uniqueNames: state.uniqueNames.filter(
            uniqueName => uniqueName != action.group.unique_name),
        };
      case actionTypes.UPDATE_GROUP:
        return {
          ...state,
          ByUniqueNames: {...state.ByUniqueNames, [action.group.unique_name]: action.group}
        };
      case actionTypes.RECEIVE_GROUPS:
        var newState = {...state};
        for (let group of action.groups) {
          if (!_.includes(newState.uniqueNames, group.unique_name)) {
            newState.uniqueNames.push(group.unique_name);
            newState.ByUniqueNames[group.unique_name] = group;
          }
          newState.ByUniqueNames[group.unique_name] = group;
        }
        return newState;
      case actionTypes.RECEIVE_GROUP:
        var newState = {...state};
        let uniqueName = action.group.unique_name;
        if (!_.includes(newState.uniqueNames, uniqueName)) {
          newState.uniqueNames.push(uniqueName);
        }
        let normalized_groups = normalize(action.group, GroupSchema).entities.groups;
        newState.ByUniqueNames[action.group.unique_name] = normalized_groups[uniqueName];
        return newState;
    }
    return state;
  };
