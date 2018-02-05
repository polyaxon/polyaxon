import {Reducer} from "redux";
import * as _ from "lodash";
import {normalize} from 'normalizr';

import {ExperimentSchema} from "../constants/schemas"
import {ExperimentAction, actionTypes} from "../actions/experiment";
import {ExperimentStateSchema, ExperimentsEmptyState} from "../models/experiment";

export const experimentsReducer: Reducer<ExperimentStateSchema> =
  (state: ExperimentStateSchema = ExperimentsEmptyState, action: ExperimentAction) => {

    switch (action.type) {
      case actionTypes.CREATE_EXPERIMENT:
        return {
          ...state,
          ByUniqueNames: {
            ...state.ByUniqueNames, [action.experiment.unique_name]: action.experiment},
          uniqueNames: [...state.uniqueNames, action.experiment.unique_name]
        };
      case actionTypes.DELETE_EXPERIMENT:
        return {
          ...state,
          ByUniqueNames: {
            ...state.ByUniqueNames,
            [action.experiment.unique_name]: {
              ...state.ByUniqueNames[action.experiment.unique_name], deleted: true}
          },
          uniqueNames: state.uniqueNames.filter(
            uniqueName => uniqueName != action.experiment.unique_name),
        };
      case actionTypes.UPDATE_EXPERIMENT:
        return {
          ...state,
          ByUniqueNames: {
            ...state.ByUniqueNames, [action.experiment.unique_name]: action.experiment}
        };
      case actionTypes.RECEIVE_EXPERIMENTS:
        var newState = {...state};
        for (let xp of action.experiments) {
          if (!_.includes(newState.uniqueNames, xp.unique_name)) {
            newState.uniqueNames.push(xp.unique_name);
            newState.ByUniqueNames[xp.unique_name] = xp;
          }
          newState.ByUniqueNames[xp.unique_name] = xp;
        }
        return newState;
      case actionTypes.RECEIVE_EXPERIMENT:
        var newState = {...state};
        let uniqueName = action.experiment.unique_name;
        if (!_.includes(newState.uniqueNames, uniqueName)) {
          newState.uniqueNames.push(uniqueName);
        }
        let normalized_experiments = normalize(action.experiment, ExperimentSchema).entities.experiments;
        newState.ByUniqueNames[action.experiment.unique_name] = normalized_experiments[uniqueName];
        return newState;
    }
    return state;
  };
