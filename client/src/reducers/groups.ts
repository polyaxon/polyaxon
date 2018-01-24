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
          byUuids: {...state.byUuids, [action.group.uuid]: action.group},
          uuids: [...state.uuids, action.group.uuid]
        };
      case actionTypes.DELETE_GROUP:
        return {
          ...state,
          byUuids: {
            ...state.byUuids,
            [action.group.uuid]: {...state.byUuids[action.group.uuid], deleted: true}
          },
          uuids: state.uuids.filter(uuid => uuid != action.group.uuid),
        };
      case actionTypes.UPDATE_GROUP:
        return {
          ...state,
          byUuids: {...state.byUuids, [action.group.uuid]: action.group}
        };
      case actionTypes.RECEIVE_GROUPS:
        var newState = {...state};
        for (let group of action.groups) {
          if (!_.includes(newState.uuids, group.uuid)) {
            newState.uuids.push(group.uuid);
            newState.byUuids[group.uuid] = group;
          }
          newState.byUuids[group.uuid] = group;
        }
        return newState;
      case actionTypes.RECEIVE_GROUP:
        var newState = {...state};
        if (!_.includes(newState.uuids, action.group.uuid)) {
          newState.uuids.push(action.group.uuid);
        }
        let normalized_groups = normalize(action.group, GroupSchema).entities.groups;
        newState.byUuids[action.group.uuid] = normalized_groups[action.group.uuid];
        return newState;
    }
    return state;
  };
