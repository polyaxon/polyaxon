import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, NotebookAction } from '../actions/notebooks';
import { NotebookSchema } from '../constants/schemas';
import { STOPPED } from '../constants/statuses';
import { NotebookModel, NotebooksEmptyState, NotebookStateSchema } from '../models/notebook';
import { LastFetchedNames } from '../models/utils';

export const notebooksReducer: Reducer<NotebookStateSchema> =
  (state: NotebookStateSchema = NotebooksEmptyState, action: NotebookAction) => {
    let newState = {...state};

    const processBuild = (notebook: NotebookModel) => {
      const uniqueName = notebook.unique_name;
      if (!_.includes(newState.lastFetched.names, uniqueName)) {
        newState.lastFetched.names.push(uniqueName);
      }
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      if (_.isNil(notebook.deleted)) {
        notebook.deleted = false;
      }
      const normalizedBuilds = normalize(notebook, NotebookSchema).entities.notebooks;
      newState.byUniqueNames[uniqueName] = {
        ...newState.byUniqueNames[uniqueName], ...normalizedBuilds[notebook.unique_name]
      };
      return newState;
    };

    switch (action.type) {
      case actionTypes.DELETE_NOTEBOOK_SUCCESS:
        return {
          ...state,
          uniqueNames: state.uniqueNames.filter(
            (name) => name !== action.notebookName),
          lastFetched: {
            ...state.lastFetched,
            names: state.lastFetched.names.filter((name) => name !== action.notebookName)
          },
        };
      case actionTypes.ARCHIVE_NOTEBOOK_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.notebookName]: {
              ...state.byUniqueNames[action.notebookName], deleted: true
            }
          },
        };
      case actionTypes.RESTORE_NOTEBOOK_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.notebookName]: {
              ...state.byUniqueNames[action.notebookName], deleted: false
            }
          },
        };
      case actionTypes.STOP_NOTEBOOK_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.notebookName]: {
              ...state.byUniqueNames[action.notebookName], last_status: STOPPED
            }
          },
        };
      case actionTypes.BOOKMARK_NOTEBOOK_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.notebookName]: {
              ...state.byUniqueNames[action.notebookName], bookmarked: true
            }
          },
        };
      case actionTypes.UNBOOKMARK_NOTEBOOK_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.notebookName]: {
              ...state.byUniqueNames[action.notebookName], bookmarked: false
            }
          },
        };
      case actionTypes.UPDATE_NOTEBOOK_SUCCESS:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.notebook.unique_name]: action.notebook}
        };
      case actionTypes.FETCH_NOTEBOOKS_REQUEST:
        newState.lastFetched = new LastFetchedNames();
        return newState;
      case actionTypes.FETCH_NOTEBOOKS_SUCCESS:
        newState.lastFetched = new LastFetchedNames();
        newState.lastFetched.count = action.count;
        for (const notebook of action.notebooks) {
          newState = processBuild(notebook);
        }
        return newState;
      case actionTypes.GET_NOTEBOOK_SUCCESS:
        return processBuild(action.notebook);
      default:
        return state;
    }
  };
