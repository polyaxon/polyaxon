import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, CodeReferenceAction } from '../actions/codeReference';
import { codeReferenceSchema } from '../constants/schemas';
import {
  CodeReferenceEmptyState,
  CodeReferenceModel,
  CodeReferenceStateSchema
} from '../models/codeReference';
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
      case actionTypes.FETCH_CODE_REFERENCE_REQUEST:
        newState.lastFetched = new LastFetchedIds();
        return newState;
      case actionTypes.FETCH_CODE_REFERENCE_SUCCESS:
        return processSearch(action.codeReference);
      default:
        return state;
    }
  };
