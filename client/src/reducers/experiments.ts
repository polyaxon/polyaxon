import { Reducer } from 'redux';
import * as _ from 'lodash';
import { normalize } from 'normalizr';

import { ExperimentSchema } from '../constants/schemas';
import { ExperimentAction, actionTypes } from '../actions/experiment';
import { ExperimentStateSchema, ExperimentsEmptyState } from '../models/experiment';
import { getExperimentIndexName } from '../constants/utils';

export const experimentsReducer: Reducer<ExperimentStateSchema> =
  (state: ExperimentStateSchema = ExperimentsEmptyState, action: ExperimentAction) => {
    let newState = {...state};
    switch (action.type) {
      case actionTypes.CREATE_EXPERIMENT:
        return {
          ...state,
          ByUniqueNames: {
            ...state.ByUniqueNames, [getExperimentIndexName(action.experiment.unique_name)]: action.experiment
          },
          uniqueNames: [...state.uniqueNames, getExperimentIndexName(action.experiment.unique_name)]
        };
      case actionTypes.DELETE_EXPERIMENT:
        return {
          ...state,
          ByUniqueNames: {
            ...state.ByUniqueNames,
            [getExperimentIndexName(action.experiment.unique_name)]: {
              ...state.ByUniqueNames[getExperimentIndexName(action.experiment.unique_name)], deleted: true
            }
          },
          uniqueNames: state.uniqueNames.filter(
            name => name !== getExperimentIndexName(action.experiment.unique_name)),
        };
      case actionTypes.UPDATE_EXPERIMENT:
        return {
          ...state,
          ByUniqueNames: {
            ...state.ByUniqueNames, [getExperimentIndexName(action.experiment.unique_name)]: action.experiment
          }
        };
      case actionTypes.RECEIVE_EXPERIMENTS:
        for (let xp of action.experiments) {
          let uniqueName = getExperimentIndexName(xp.unique_name);
          if (!_.includes(newState.uniqueNames, uniqueName)) {
            newState.uniqueNames.push(uniqueName);
            newState.ByUniqueNames[uniqueName] = xp;
          }
          newState.ByUniqueNames[uniqueName] = xp;
        }
        return newState;
      case actionTypes.RECEIVE_EXPERIMENT:
        let uniqueName = getExperimentIndexName(action.experiment.unique_name);
        if (!_.includes(newState.uniqueNames, uniqueName)) {
          newState.uniqueNames.push(uniqueName);
        }
        let normalizedExperiments = normalize(action.experiment, ExperimentSchema).entities.experiments;
        newState.ByUniqueNames[uniqueName] = normalizedExperiments[action.experiment.unique_name];
        return newState;
    }
    return state;
  };
