import {Action} from "redux";
import {ExperimentModel} from "../models/experiment";


export enum actionTypes {
    CREATE_EXPERIMENT,
    DELETE_EXPERIMENT,
    UPDATE_EXPERIMENT,
}

export interface ExperimentAction extends Action {
	experiments: ExperimentModel[];
}

export function createExperiment(): ExperimentAction {
    return {
      type: actionTypes.CREATE_EXPERIMENT,
      experiments: []
    }
}

export function deleteExperiment(): ExperimentAction {
    return {
      type: actionTypes.DELETE_EXPERIMENT,
      experiments: []
    }
}

export function updateExperiment(): ExperimentAction {
    return {
      type: actionTypes.UPDATE_EXPERIMENT,
      experiments: []
    }
}
