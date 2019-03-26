import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, NotebookAction } from '../actions/notebooks';
import { ACTIONS } from '../constants/actions';
import { NotebookSchema } from '../constants/schemas';
import { STOPPED } from '../constants/statuses';
import { AlertEmptyState, AlertSchema, processErrorById, processErrorGlobal } from '../models/alerts';
import {
  LoadingIndicatorEmptyState,
  LoadingIndicatorSchema,
  processLoadingIndicatorById,
  processLoadingIndicatorGlobal
} from '../models/loadingIndicator';
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

export const LoadingIndicatorNotebooksReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: NotebookAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_NOTEBOOK_REQUEST:
        return {
          ...state,
          notebooks: processLoadingIndicatorById(state.notebooks, action.notebookName, true, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_NOTEBOOK_ERROR:
      case actionTypes.UPDATE_NOTEBOOK_SUCCESS:
        return {
          ...state,
          notebooks: processLoadingIndicatorById(state.notebooks, action.notebookName, false, ACTIONS.UPDATE)
        };

      case actionTypes.GET_NOTEBOOK_REQUEST:
        return {
          ...state,
          notebooks: processLoadingIndicatorGlobal(
            processLoadingIndicatorById(state.notebooks, action.notebookName, true, ACTIONS.GET),
            false,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_NOTEBOOK_ERROR:
      case actionTypes.GET_NOTEBOOK_SUCCESS:
        return {
          ...state,
          notebooks: processLoadingIndicatorById(state.notebooks, action.notebookName, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_NOTEBOOK_REQUEST:
        return {
          ...state,
          notebooks: processLoadingIndicatorById(state.notebooks, action.notebookName, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_NOTEBOOK_ERROR:
      case actionTypes.DELETE_NOTEBOOK_SUCCESS:
        return {
          ...state,
          notebooks: processLoadingIndicatorById(state.notebooks, action.notebookName, false, ACTIONS.DELETE)
        };

      case actionTypes.ARCHIVE_NOTEBOOK_REQUEST:
        return {
          ...state,
          notebooks: processLoadingIndicatorById(state.notebooks, action.notebookName, true, ACTIONS.ARCHIVE)
        };
      case actionTypes.ARCHIVE_NOTEBOOK_ERROR:
      case actionTypes.ARCHIVE_NOTEBOOK_SUCCESS:
        return {
          ...state,
          notebooks: processLoadingIndicatorById(state.notebooks, action.notebookName, false, ACTIONS.ARCHIVE)
        };

      case actionTypes.RESTORE_NOTEBOOK_REQUEST:
        return {
          ...state,
          notebooks: processLoadingIndicatorById(state.notebooks, action.notebookName, true, ACTIONS.RESTORE)
        };
      case actionTypes.RESTORE_NOTEBOOK_ERROR:
      case actionTypes.RESTORE_NOTEBOOK_SUCCESS:
        return {
          ...state,
          notebooks: processLoadingIndicatorById(state.notebooks, action.notebookName, false, ACTIONS.RESTORE)
        };

      case actionTypes.STOP_NOTEBOOK_REQUEST:
        return {
          ...state,
          notebooks: processLoadingIndicatorById(state.notebooks, action.notebookName, true, ACTIONS.STOP)
        };
      case actionTypes.STOP_NOTEBOOK_ERROR:
      case actionTypes.STOP_NOTEBOOK_SUCCESS:
        return {
          ...state,
          notebooks: processLoadingIndicatorById(state.notebooks, action.notebookName, false, ACTIONS.STOP)
        };

      case actionTypes.BOOKMARK_NOTEBOOK_REQUEST:
        return {
          ...state,
          notebooks: processLoadingIndicatorById(state.notebooks, action.notebookName, true, ACTIONS.BOOKMARK)
        };
      case actionTypes.BOOKMARK_NOTEBOOK_ERROR:
      case actionTypes.BOOKMARK_NOTEBOOK_SUCCESS:
        return {
          ...state,
          notebooks: processLoadingIndicatorById(state.notebooks, action.notebookName, false, ACTIONS.BOOKMARK)
        };

      case actionTypes.UNBOOKMARK_NOTEBOOK_REQUEST:
        return {
          ...state,
          notebooks: processLoadingIndicatorById(state.notebooks, action.notebookName, true, ACTIONS.UNBOOKMARK)
        };
      case actionTypes.UNBOOKMARK_NOTEBOOK_ERROR:
      case actionTypes.UNBOOKMARK_NOTEBOOK_SUCCESS:
        return {
          ...state,
          notebooks: processLoadingIndicatorById(state.notebooks, action.notebookName, false, ACTIONS.UNBOOKMARK)
        };

      case actionTypes.FETCH_NOTEBOOKS_REQUEST:
        return {
          ...state,
          notebooks: processLoadingIndicatorGlobal(state.notebooks, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_NOTEBOOKS_ERROR:
      case actionTypes.FETCH_NOTEBOOKS_SUCCESS:
        return {
          ...state,
          notebooks: processLoadingIndicatorGlobal(state.notebooks, false, ACTIONS.FETCH)
        };
      default:
        return state;
    }
  };

export const AlertNotebooksReducer: Reducer<AlertSchema> =
  (state: AlertSchema = AlertEmptyState, action: NotebookAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_NOTEBOOK_REQUEST:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, null, null, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_NOTEBOOK_SUCCESS:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, null, true, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_NOTEBOOK_ERROR:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, action.error, false, ACTIONS.UPDATE)
        };

      case actionTypes.GET_NOTEBOOK_REQUEST:
        return {
          ...state,
          notebooks: processErrorGlobal(
            processErrorById(state.notebooks, action.notebookName, null, null, ACTIONS.GET),
            null,
            null,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_NOTEBOOK_SUCCESS:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, null, true, ACTIONS.GET)
        };
      case actionTypes.GET_NOTEBOOK_ERROR:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, action.error, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_NOTEBOOK_REQUEST:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, null, null, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_NOTEBOOK_SUCCESS:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, null, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_NOTEBOOK_ERROR:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, action.error, false, ACTIONS.DELETE)
        };

      case actionTypes.ARCHIVE_NOTEBOOK_REQUEST:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, null, null, ACTIONS.ARCHIVE)
        };
      case actionTypes.ARCHIVE_NOTEBOOK_SUCCESS:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, null, true, ACTIONS.ARCHIVE)
        };
      case actionTypes.ARCHIVE_NOTEBOOK_ERROR:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, action.error, false, ACTIONS.ARCHIVE)
        };

      case actionTypes.RESTORE_NOTEBOOK_REQUEST:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, null, null, ACTIONS.RESTORE)
        };
      case actionTypes.RESTORE_NOTEBOOK_SUCCESS:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, null, true, ACTIONS.RESTORE)
        };
      case actionTypes.RESTORE_NOTEBOOK_ERROR:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, action.error, false, ACTIONS.RESTORE)
        };

      case actionTypes.STOP_NOTEBOOK_REQUEST:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, null, null, ACTIONS.STOP)
        };
      case actionTypes.STOP_NOTEBOOK_SUCCESS:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, null, true, ACTIONS.STOP)
        };
      case actionTypes.STOP_NOTEBOOK_ERROR:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, action.error, false, ACTIONS.STOP)
        };

      case actionTypes.BOOKMARK_NOTEBOOK_REQUEST:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, null, null, ACTIONS.BOOKMARK)
        };
      case actionTypes.BOOKMARK_NOTEBOOK_SUCCESS:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, null, true, ACTIONS.BOOKMARK)
        };
      case actionTypes.BOOKMARK_NOTEBOOK_ERROR:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, action.error, false, ACTIONS.BOOKMARK)
        };

      case actionTypes.UNBOOKMARK_NOTEBOOK_REQUEST:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, null, null, ACTIONS.UNBOOKMARK)
        };
      case actionTypes.UNBOOKMARK_NOTEBOOK_SUCCESS:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, null, true, ACTIONS.UNBOOKMARK)
        };
      case actionTypes.UNBOOKMARK_NOTEBOOK_ERROR:
        return {
          ...state,
          notebooks: processErrorById(state.notebooks, action.notebookName, action.error, null, ACTIONS.UNBOOKMARK)
        };

      case actionTypes.FETCH_NOTEBOOKS_REQUEST:
        return {
          ...state,
          notebooks: processErrorGlobal(state.notebooks, null, null, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_NOTEBOOKS_SUCCESS:
         return {
          ...state,
          notebooks: processErrorGlobal(state.notebooks, null, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_NOTEBOOKS_ERROR:
        return {
          ...state,
          notebooks: processErrorGlobal(state.notebooks, action.error, false, ACTIONS.FETCH)
        };
      default:
        return state;
    }
  };
