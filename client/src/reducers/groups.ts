import * as _ from 'lodash';
import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import { actionTypes, GroupAction } from '../actions/groups';
import { ACTIONS } from '../constants/actions';
import { GroupSchema } from '../constants/schemas';
import { STOPPING } from '../constants/statuses';
import { ErrorEmptyState, ErrorSchema, processErrorById, processErrorGlobal } from '../models/errors';
import { GroupModel, GroupsEmptyState, GroupStateSchema } from '../models/group';
import {
  LoadingIndicatorEmptyState,
  LoadingIndicatorSchema,
  processLoadingIndicatorById,
  processLoadingIndicatorGlobal
} from '../models/loadingIndicator';
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

export const LoadingIndicatorGroupReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: GroupAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_GROUP_REQUEST:
        return {
          ...state,
          groups: processLoadingIndicatorById(state.groups, action.groupName, true, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_GROUP_ERROR:
      case actionTypes.UPDATE_GROUP_SUCCESS:
        return {
          ...state,
          groups: processLoadingIndicatorById(state.groups, action.groupName, false, ACTIONS.UPDATE)
        };

      case actionTypes.GET_GROUP_REQUEST:
        return {
          ...state,
          groups: processLoadingIndicatorGlobal(
            processLoadingIndicatorById(state.groups, action.groupName, true, ACTIONS.GET),
            false,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_GROUP_ERROR:
      case actionTypes.GET_GROUP_SUCCESS:
        return {
          ...state,
          groups: processLoadingIndicatorById(state.groups, action.groupName, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_GROUP_REQUEST:
        return {
          ...state,
          groups: processLoadingIndicatorById(state.groups, action.groupName, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_GROUP_ERROR:
      case actionTypes.DELETE_GROUP_SUCCESS:
        return {
          ...state,
          groups: processLoadingIndicatorById(state.groups, action.groupName, false, ACTIONS.DELETE)
        };

      case actionTypes.ARCHIVE_GROUP_REQUEST:
        return {
          ...state,
          groups: processLoadingIndicatorById(state.groups, action.groupName, true, ACTIONS.ARCHIVE)
        };
      case actionTypes.ARCHIVE_GROUP_ERROR:
      case actionTypes.ARCHIVE_GROUP_SUCCESS:
        return {
          ...state,
          groups: processLoadingIndicatorById(state.groups, action.groupName, false, ACTIONS.ARCHIVE)
        };

      case actionTypes.RESTORE_GROUP_REQUEST:
        return {
          ...state,
          groups: processLoadingIndicatorById(state.groups, action.groupName, true, ACTIONS.RESTORE)
        };
      case actionTypes.RESTORE_GROUP_ERROR:
      case actionTypes.RESTORE_GROUP_SUCCESS:
        return {
          ...state,
          groups: processLoadingIndicatorById(state.groups, action.groupName, false, ACTIONS.RESTORE)
        };

      case actionTypes.STOP_GROUP_REQUEST:
        return {
          ...state,
          groups: processLoadingIndicatorById(state.groups, action.groupName, true, ACTIONS.STOP)
        };
      case actionTypes.STOP_GROUP_ERROR:
      case actionTypes.STOP_GROUP_SUCCESS:
        return {
          ...state,
          groups: processLoadingIndicatorById(state.groups, action.groupName, false, ACTIONS.STOP)
        };

      case actionTypes.BOOKMARK_GROUP_REQUEST:
        return {
          ...state,
          groups: processLoadingIndicatorById(state.groups, action.groupName, true, ACTIONS.BOOKMARK)
        };
      case actionTypes.BOOKMARK_GROUP_ERROR:
      case actionTypes.BOOKMARK_GROUP_SUCCESS:
        return {
          ...state,
          groups: processLoadingIndicatorById(state.groups, action.groupName, false, ACTIONS.BOOKMARK)
        };

      case actionTypes.UNBOOKMARK_GROUP_REQUEST:
        return {
          ...state,
          groups: processLoadingIndicatorById(state.groups, action.groupName, true, ACTIONS.UNBOOKMARK)
        };
      case actionTypes.UNBOOKMARK_GROUP_ERROR:
      case actionTypes.UNBOOKMARK_GROUP_SUCCESS:
        return {
          ...state,
          groups: processLoadingIndicatorById(state.groups, action.groupName, false, ACTIONS.UNBOOKMARK)
        };

      case actionTypes.START_GROUP_TENSORBOARD_REQUEST:
        return {
          ...state,
          groups: processLoadingIndicatorById(state.groups,
                                              action.groupName,
                                              true,
                                              ACTIONS.START_TENSORBOARD)
        };
      case actionTypes.START_GROUP_TENSORBOARD_ERROR:
      case actionTypes.START_GROUP_TENSORBOARD_SUCCESS:
        return {
          ...state,
          groups: processLoadingIndicatorById(state.groups,
                                              action.groupName,
                                              false,
                                              ACTIONS.START_TENSORBOARD)
        };

      case actionTypes.STOP_GROUP_TENSORBOARD_REQUEST:
        return {
          ...state,
          groups: processLoadingIndicatorById(state.groups,
                                              action.groupName,
                                              true,
                                              ACTIONS.STOP_TENSORBOARD)
        };
      case actionTypes.STOP_GROUP_TENSORBOARD_ERROR:
      case actionTypes.STOP_GROUP_TENSORBOARD_SUCCESS:
        return {
          ...state,
          groups: processLoadingIndicatorById(
            state.groups,
            action.groupName,
            false,
            ACTIONS.STOP_TENSORBOARD)
        };

      case actionTypes.FETCH_GROUPS_REQUEST:
        return {
          ...state,
          groups: processLoadingIndicatorGlobal(state.groups, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_GROUPS_ERROR:
      case actionTypes.FETCH_GROUPS_SUCCESS:
        return {
          ...state,
          groups: processLoadingIndicatorGlobal(state.groups, false, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_GROUP_REQUEST:
        return {
          ...state,
          groups: processLoadingIndicatorGlobal(state.groups, true, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_GROUP_ERROR:
        return {
          ...state,
          groups: processLoadingIndicatorGlobal(state.groups, false, ACTIONS.CREATE)
        };
      default:
        return state;
    }
  };

export const ErrorGroupReducer: Reducer<ErrorSchema> =
  (state: ErrorSchema = ErrorEmptyState, action: GroupAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_GROUP_REQUEST:
      case actionTypes.UPDATE_GROUP_SUCCESS:
        return {
          ...state,
          groups: processErrorById(state.groups, action.groupName, null, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_GROUP_ERROR:
        return {
          ...state,
          groups: processErrorById(state.groups, action.groupName, action.error, ACTIONS.UPDATE)
        };

      case actionTypes.GET_GROUP_REQUEST:
      case actionTypes.GET_GROUP_SUCCESS:
        return {
          ...state,
          groups: processErrorGlobal(
            processErrorById(state.groups, action.groupName, null, ACTIONS.GET),
            null,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_GROUP_ERROR:
        return {
          ...state,
          groups: processErrorById(state.groups, action.groupName, action.error, ACTIONS.GET)
        };

      case actionTypes.DELETE_GROUP_REQUEST:
      case actionTypes.DELETE_GROUP_SUCCESS:
        return {
          ...state,
          groups: processErrorById(state.groups, action.groupName, null, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_GROUP_ERROR:
        return {
          ...state,
          groups: processErrorById(state.groups, action.groupName, action.error, ACTIONS.DELETE)
        };

      case actionTypes.ARCHIVE_GROUP_REQUEST:
      case actionTypes.ARCHIVE_GROUP_SUCCESS:
        return {
          ...state,
          groups: processErrorById(state.groups, action.groupName, null, ACTIONS.ARCHIVE)
        };
      case actionTypes.ARCHIVE_GROUP_ERROR:
        return {
          ...state,
          groups: processErrorById(state.groups, action.groupName, action.error, ACTIONS.ARCHIVE)
        };

      case actionTypes.RESTORE_GROUP_REQUEST:
      case actionTypes.RESTORE_GROUP_SUCCESS:
        return {
          ...state,
          groups: processErrorById(state.groups, action.groupName, null, ACTIONS.RESTORE)
        };
      case actionTypes.RESTORE_GROUP_ERROR:
        return {
          ...state,
          groups: processErrorById(state.groups, action.groupName, action.error, ACTIONS.RESTORE)
        };

      case actionTypes.STOP_GROUP_REQUEST:
      case actionTypes.STOP_GROUP_SUCCESS:
        return {
          ...state,
          groups: processErrorById(state.groups, action.groupName, null, ACTIONS.STOP)
        };
      case actionTypes.STOP_GROUP_ERROR:
        return {
          ...state,
          groups: processErrorById(state.groups, action.groupName, action.error, ACTIONS.STOP)
        };

      case actionTypes.BOOKMARK_GROUP_REQUEST:
      case actionTypes.BOOKMARK_GROUP_SUCCESS:
        return {
          ...state,
          groups: processErrorById(state.groups, action.groupName, null, ACTIONS.BOOKMARK)
        };
      case actionTypes.BOOKMARK_GROUP_ERROR:
        return {
          ...state,
          groups: processErrorById(state.groups, action.groupName, action.error, ACTIONS.BOOKMARK)
        };

      case actionTypes.UNBOOKMARK_GROUP_REQUEST:
      case actionTypes.UNBOOKMARK_GROUP_SUCCESS:
        return {
          ...state,
          groups: processErrorById(state.groups, action.groupName, null, ACTIONS.UNBOOKMARK)
        };
      case actionTypes.UNBOOKMARK_GROUP_ERROR:
        return {
          ...state,
          groups: processErrorById(state.groups, action.groupName, action.error, ACTIONS.UNBOOKMARK)
        };

      case actionTypes.START_GROUP_TENSORBOARD_REQUEST:
      case actionTypes.START_GROUP_TENSORBOARD_SUCCESS:
        return {
          ...state,
          groups: processErrorById(state.groups,
                                   action.groupName,
                                   null,
                                   ACTIONS.START_TENSORBOARD)
        };
      case actionTypes.START_GROUP_TENSORBOARD_ERROR:
        return {
          ...state,
          groups: processErrorById(state.groups,
                                   action.groupName,
                                   action.error,
                                   ACTIONS.START_TENSORBOARD)
        };

      case actionTypes.STOP_GROUP_TENSORBOARD_REQUEST:
      case actionTypes.STOP_GROUP_TENSORBOARD_SUCCESS:
        return {
          ...state,
          groups: processErrorById(state.groups,
                                   action.groupName,
                                   null,
                                   ACTIONS.STOP_TENSORBOARD)
        };
      case actionTypes.STOP_GROUP_TENSORBOARD_ERROR:
        return {
          ...state,
          groups: processErrorById(
            state.groups,
            action.groupName,
            action.error,
            ACTIONS.STOP_TENSORBOARD)
        };

      case actionTypes.FETCH_GROUPS_REQUEST:
      case actionTypes.FETCH_GROUPS_SUCCESS:
        return {
          ...state,
          groups: processErrorGlobal(state.groups, null, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_GROUPS_ERROR:
        return {
          ...state,
          groups: processErrorGlobal(state.groups, action.error, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_GROUP_REQUEST:
        return {
          ...state,
          groups: processErrorGlobal(state.groups, null, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_GROUP_ERROR:
        return {
          ...state,
          groups: processErrorGlobal(state.groups, action.error, ACTIONS.CREATE)
        };
      default:
        return state;
    }
  };
