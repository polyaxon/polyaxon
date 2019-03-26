import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, CodeReferenceAction } from '../actions/codeReference';
import { ACTIONS } from '../constants/actions';
import { codeReferenceSchema } from '../constants/schemas';
import { AlertEmptyState, AlertSchema, processErrorById, processErrorGlobal } from '../models/alerts';
import { CodeReferenceEmptyState, CodeReferenceModel, CodeReferenceStateSchema } from '../models/codeReference';
import {
  LoadingIndicatorEmptyState,
  LoadingIndicatorSchema,
  processLoadingIndicatorById,
  processLoadingIndicatorGlobal
} from '../models/loadingIndicator';
import { LastFetchedIds } from '../models/utils';

export const codeReferencesReducer: Reducer<CodeReferenceStateSchema> =
  (state: CodeReferenceStateSchema = CodeReferenceEmptyState, action: CodeReferenceAction) => {
    const newState = {...state};

    const processSearch = (codeReference: CodeReferenceModel) => {
      newState.lastFetched.ids.push(codeReference.id);
      if (!_.includes(newState.ids, codeReference.id)) {
        newState.ids.push(codeReference.id);
      }
      const normalizedBuilds = normalize(codeReference, codeReferenceSchema).entities.codeReferences;
      newState.byIds[codeReference.id] = {
        ...newState.byIds[codeReference.id], ...normalizedBuilds[codeReference.id]
      };
      return newState;
    };

    switch (action.type) {
      case actionTypes.GET_CODE_REFERENCE_REQUEST:
        newState.lastFetched = new LastFetchedIds();
        return newState;
      case actionTypes.GET_CODE_REFERENCE_SUCCESS:
        return processSearch(action.codeReference);
      default:
        return state;
    }
  };

export const LoadingIndicatorCodeReferenceReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: CodeReferenceAction) => {
    switch (action.type) {
      case actionTypes.GET_CODE_REFERENCE_REQUEST:
        return {
          ...state,
          codeReference: processLoadingIndicatorGlobal(
            processLoadingIndicatorById(state.codeReference, 0, true, ACTIONS.GET),
            false,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_CODE_REFERENCE_ERROR:
      case actionTypes.GET_CODE_REFERENCE_SUCCESS:
        return {
          ...state,
          codeReference: processLoadingIndicatorById(state.codeReference, 0, false, ACTIONS.GET)
        };
      default:
        return state;
    }
  };

export const AlertCodeReferenceReducer: Reducer<AlertSchema> =
  (state: AlertSchema = AlertEmptyState, action: CodeReferenceAction) => {
    switch (action.type) {
      case actionTypes.GET_CODE_REFERENCE_REQUEST:
        return {
          ...state,
          codeReference: processErrorGlobal(
            processErrorById(state.codeReference, 0, null, null, ACTIONS.GET),
            null,
            null,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_CODE_REFERENCE_SUCCESS:
        return {
          ...state,
          codeReference: processErrorById(state.codeReference, 0, null, true, ACTIONS.GET)
        };
      case actionTypes.GET_CODE_REFERENCE_ERROR:
        return {
          ...state,
          codeReference: processErrorById(state.codeReference, 0, action.error, false, ACTIONS.GET)
        };
      default:
        return state;
    }
  };
