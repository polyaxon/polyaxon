import * as _ from 'lodash';
import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import { actionTypes, OptionAction } from '../actions/options';
import { ACTIONS } from '../constants/actions';
import { OptionSchema } from '../constants/schemas';
import { AlertEmptyState, AlertSchema, processErrorById } from '../models/alerts';
import {
  LoadingIndicatorEmptyState,
  LoadingIndicatorSchema,
  processLoadingIndicatorById,
} from '../models/loadingIndicator';
import { OptionModel, OptionsEmptyState, OptionStateSchema } from '../models/option';
import { LastFetchedNames } from '../models/utils';

export const optionsReducer: Reducer<OptionStateSchema> =
  (state: OptionStateSchema = OptionsEmptyState, action: OptionAction) => {
    let newState = {...state};

    const processOption = (option: OptionModel) => {
      if (!_.includes(newState.lastFetched.names, option.key)) {
        newState.lastFetched.names.push(option.key);
      }
      if (!_.includes(newState.uniqueNames, option.key)) {
        newState.uniqueNames.push(option.key);
      }
      const normalizedOptions = normalize(option, OptionSchema).entities.options;
      newState.byUniqueNames[option.key] = {
        ...newState.byUniqueNames[option.key],
        ...normalizedOptions[option.key]
      };
      return newState;
    };

    switch (action.type) {
      case actionTypes.FETCH_OPTIONS_SUCCESS:
        newState.lastFetched = new LastFetchedNames();
        newState.lastFetched.count = action.count;
        for (const option of action.options) {
          newState = processOption(option);
        }
        return newState;
      default:
        return state;
    }
  };

export const LoadingIndicatorOptionsReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: OptionAction) => {
    switch (action.type) {
      case actionTypes.POST_OPTIONS_REQUEST:
        return {
          ...state,
          options: processLoadingIndicatorById(state.options, action.section, true, ACTIONS.UPDATE)
        };
      case actionTypes.POST_OPTIONS_ERROR:
      case actionTypes.POST_OPTIONS_SUCCESS:
        return {
          ...state,
          options: processLoadingIndicatorById(state.options, action.section, false, ACTIONS.UPDATE)
        };

      case actionTypes.FETCH_OPTIONS_REQUEST:
        return {
          ...state,
          options: processLoadingIndicatorById(state.options, action.section, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_OPTIONS_ERROR:
      case actionTypes.FETCH_OPTIONS_SUCCESS:
        return {
          ...state,
          options: processLoadingIndicatorById(state.options, action.section, false, ACTIONS.FETCH)
        };
      default:
        return state;
    }
};

export const AlertOptionsReducer: Reducer<AlertSchema> =
  (state: AlertSchema = AlertEmptyState, action: OptionAction) => {
    switch (action.type) {
      case actionTypes.POST_OPTIONS_REQUEST:
        return {
          ...state,
          options: processErrorById(state.options, action.section, null, null, ACTIONS.UPDATE)
        };
      case actionTypes.POST_OPTIONS_SUCCESS:
        return {
          ...state,
          options: processErrorById(state.options, action.section, null, true, ACTIONS.UPDATE)
        };
      case actionTypes.POST_OPTIONS_ERROR:
        return {
          ...state,
          options: processErrorById(state.options, action.section, action.error, false, ACTIONS.UPDATE)
        };

      case actionTypes.FETCH_OPTIONS_REQUEST:
        return {
          ...state,
          options: processErrorById(state.options, action.section, null, null, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_OPTIONS_SUCCESS:
        return {
          ...state,
          options: processErrorById(state.options, action.section, null, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_OPTIONS_ERROR:
        return {
          ...state,
          options: processErrorById(state.options, action.section, action.error, false, ACTIONS.FETCH)
        };
      default:
        return state;
    }
  };
