import { Reducer } from 'redux';
import * as _ from 'lodash';
import { normalize } from 'normalizr';

import { GroupSchema } from '../constants/schemas';
import { GroupAction, actionTypes } from '../actions/group';
import { GroupStateSchema, GroupsEmptyState, GroupModel } from '../models/group';
import { ProjectsEmptyState, ProjectStateSchema } from '../models/project';

export const groupsReducer: Reducer<GroupStateSchema> =
  (state: GroupStateSchema = GroupsEmptyState, action: GroupAction) => {
    let newState = {...state};

    let processGroup = function(group: GroupModel) {
      let uniqueName = group.unique_name;
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      let normalizedGroups = normalize(group, GroupSchema).entities.groups;
      newState.byUniqueNames[uniqueName] = {
        ...newState.byUniqueNames[uniqueName], ...normalizedGroups[uniqueName]
      };
      if (newState.byUniqueNames[uniqueName].experiments == null) {
        newState.byUniqueNames[uniqueName].experiments = [];
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.CREATE_GROUP:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.group.unique_name]: action.group},
          uniqueNames: [...state.uniqueNames, action.group.unique_name]
        };
      case actionTypes.DELETE_GROUP:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.group.unique_name]: {
              ...state.byUniqueNames[action.group.unique_name], deleted: true}
          },
          uniqueNames: state.uniqueNames.filter(
            name => name !== action.group.unique_name),
        };
      case actionTypes.UPDATE_GROUP:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.group.unique_name]: action.group}
        };
      case actionTypes.RECEIVE_GROUPS:
        for (let group of action.groups) {
          newState = processGroup(group);
        }
        return newState;
      case actionTypes.RECEIVE_GROUP:
        return processGroup(action.group);
      default:
        return state;
    }
  };

export const ProjectGroupsReducer: Reducer<ProjectStateSchema> =
  (state: ProjectStateSchema = ProjectsEmptyState, action: GroupAction) => {
    let newState = {...state};

    let processGroup = function (group: GroupModel) {
      let projectName = group.project;
      if (_.includes(newState.uniqueNames, projectName) &&
        !_.includes(newState.byUniqueNames[projectName].groups, group.unique_name)) {
        newState.byUniqueNames[projectName].groups.push(group.unique_name);
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.RECEIVE_GROUP:
        return processGroup(action.group);
      case actionTypes.RECEIVE_GROUPS:
        for (let experiment of action.groups) {
          newState = processGroup(experiment);
        }
        return newState;
      default:
        return state;
    }
  };
