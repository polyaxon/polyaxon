import {Reducer} from "redux";
import {ExperimentAction, actionTypes} from "../actions/experiment";
import {ExperimentModel} from "../models/experiment";

export const experimentsReducer: Reducer<ExperimentModel[]> =
	(state: ExperimentModel[] = [
	  {id: Math.floor(Math.random() * 60) + 1  , name: 'name'},
    {id: Math.floor(Math.random() * 60) + 1  , name: 'babla'}] as ExperimentModel[],
  action: ExperimentAction) => {

  switch (action.type) {
    case actionTypes.CREATE_EXPERIMENT:
      return [...state, action.experiment];
    case actionTypes.DELETE_EXPERIMENT:
      return state.filter(xp => xp.id != action.experimentId);
    case actionTypes.UPDATE_EXPERIMENT:
      return state.map(xp => xp.id === action.experiment.id? action.experiment: xp);
  }
  return state;
};
