import {Reducer} from "redux";
import * as _ from "lodash";

import {ExperimentAction, actionTypes} from "../actions/experiment";
import {ExperimentStateSchema, ExperimentsEmptyState} from "../models/experiment";

export const experimentsReducer: Reducer<ExperimentStateSchema> =
	(state: ExperimentStateSchema = ExperimentsEmptyState, action: ExperimentAction) => {

  switch (action.type) {
    case actionTypes.CREATE_EXPERIMENT:
      return {
        ...state,
        byIds: {...state.byIds, [action.experiment.id] : action.experiment},
        ids: [...state.ids, action.experiment.id]
      };
    case actionTypes.DELETE_EXPERIMENT:
      return {
        ...state,
        byIds: {...state.byIds, [action.experimentId] : {...state.byIds[action.experimentId], deleted:true}},
        ids: state.ids.filter(id => id != action.experimentId),
      };
    case actionTypes.UPDATE_EXPERIMENT:
      return {
        ...state,
        byIds: {...state.byIds, [action.experiment.id]: action.experiment}
      };
    case actionTypes.RECEIVE_EXPERIMENTS:
      var newState = {...state};
      for (let xp of action.experiments) {
        if (!_.includes(newState.ids, xp.id)) {
          newState.ids.push(xp.id);
          newState.byIds[xp.id] = xp;
        }
        newState.byIds[xp.id] = xp;
      }
      return newState;
  }
  return state;
};
