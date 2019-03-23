import * as _ from 'lodash';
import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import { actionTypes, GroupAction } from '../actions/groups';
import { GroupSchema } from '../constants/schemas';
import { STOPPING } from '../constants/statuses';
import { GroupModel, GroupsEmptyState, GroupStateSchema } from '../models/group';
import { ProjectsEmptyState, ProjectStateSchema } from '../models/project';
import { LastFetchedNames } from '../models/utils';

export const groupsReducer: Reducer<GroupStateSchema> =
  (state: GroupStateSchema = GroupsEmptyState, action: GroupAction) => {
    let newState = {...state};

    const setGroupRelated = (group: GroupModel) => {
      if (group.experiments == null) {
        group.experiments = [];
      }
      return group;
    };

    const processGroup = (group: GroupModel) => {
      const uniqueName = group.unique_name;
      if (!_.includes(newState.lastFetched.names, uniqueName)) {
        newState.lastFetched.names.push(uniqueName);
      }
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      if (_.isNil(group.deleted)) {
        group.deleted = false;
      }
      const normalizedGroups = normalize(group, GroupSchema).entities.groups;
      newState.byUniqueNames[uniqueName] = {
        ...newState.byUniqueNames[uniqueName], ...normalizedGroups[uniqueName]
      };
      setGroupRelated(newState.byUniqueNames[uniqueName]);

      return newState;
    };

    switch (action.type) {
      case actionTypes.DELETE_GROUP_SUCCESS:
        return {
          ...state,
          uniqueNames: state.uniqueNames.filter(
            (name) => name !== action.groupName),
          lastFetched: {
            ...state.lastFetched,
            names: state.lastFetched.names.filter((name) => name !== action.groupName)
          },
        };
      case actionTypes.ARCHIVE_GROUP_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.groupName]: {
              ...state.byUniqueNames[action.groupName], deleted: true
            }
          },
        };
      case actionTypes.RESTORE_GROUP_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.groupName]: {
              ...state.byUniqueNames[action.groupName], deleted: false
            }
          },
        };
      case actionTypes.STOP_GROUP_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.groupName]: {
              ...state.byUniqueNames[action.groupName], last_status: STOPPING
            }
          },
        };
      case actionTypes.BOOKMARK_GROUP_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.groupName]: {
              ...state.byUniqueNames[action.groupName], bookmarked: true
            }
          },
        };
      case actionTypes.UNBOOKMARK_GROUP_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.groupName]: {
              ...state.byUniqueNames[action.groupName], bookmarked: false
            }
          },
        };
      case actionTypes.STOP_GROUP_TENSORBOARD_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.groupName]: {
              ...state.byUniqueNames[action.groupName], has_tensorboard: false
            }
          },
        };
      case actionTypes.UPDATE_GROUP_SUCCESS:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.group.unique_name]: setGroupRelated(action.group)}
        };
      case actionTypes.FETCH_GROUPS_REQUEST:
        newState.lastFetched = new LastFetchedNames();
        return newState;
      case actionTypes.FETCH_GROUPS_SUCCESS:
        newState.lastFetched = new LastFetchedNames();
        newState.lastFetched.count = action.count;
        for (const group of action.groups) {
          newState = processGroup(group);
        }
        return newState;
      case actionTypes.GET_GROUP_SUCCESS:
        return processGroup(action.group);
      default:
        return state;
    }
  };

export const ProjectGroupsReducer: Reducer<ProjectStateSchema> =
  (state: ProjectStateSchema = ProjectsEmptyState, action: GroupAction) => {
    let newState = {...state};

    const processGroup = (group: GroupModel) => {
      const projectName = group.project;
      if (_.includes(newState.uniqueNames, projectName) &&
        !_.includes(newState.byUniqueNames[projectName].groups, group.unique_name)) {
        newState.byUniqueNames[projectName].groups.push(group.unique_name);
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.GET_GROUP_SUCCESS:
        return processGroup(action.group);
      case actionTypes.FETCH_GROUPS_SUCCESS:
        for (const experiment of action.groups) {
          newState = processGroup(experiment);
        }
        return newState;
      default:
        return state;
    }
  };
