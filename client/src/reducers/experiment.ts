import {Reducer} from "redux";
import {ExperimentAction, actionTypes} from "../actions/experiment";
import {ExperimentModel} from "../models/experiment";

export const experimentReducer: Reducer<ExperimentModel[]> =
	(state: ExperimentModel[] =[], action: ExperimentAction) => {

  switch (action.type) {
    case actionTypes.CREATE_EXPERIMENT:
      return state;
    case actionTypes.DELETE_EXPERIMENT:
      return state;
    case actionTypes.UPDATE_EXPERIMENT:
      return state;
  }
  return state;
};
