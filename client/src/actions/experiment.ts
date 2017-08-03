import {Action} from "redux";
import {ExperimentModel} from "../models/experiment";


export enum actionTypes {
    CREATE_EXPERIMENT='CREATE_EXPERIMENT',
    DELETE_EXPERIMENT='DELETE_EXPERIMENT',
    UPDATE_EXPERIMENT='UPDATE_EXPERIMENT',
}

export interface CreateUpdateExperimentAction extends Action {
  type: actionTypes.CREATE_EXPERIMENT | actionTypes.UPDATE_EXPERIMENT;
  experiment: ExperimentModel
}

export interface DeleteExperimentAction extends Action {
  type: actionTypes.DELETE_EXPERIMENT;
  experimentId: number
}

export type ExperimentAction = CreateUpdateExperimentAction | DeleteExperimentAction;

export function createExperiment(experiment: ExperimentModel): ExperimentAction {
    return {
      type: actionTypes.CREATE_EXPERIMENT,
      experiment
    }
}

export function updateExperiment(experiment: ExperimentModel): ExperimentAction {
    return {
      type: actionTypes.UPDATE_EXPERIMENT,
      experiment
    }
}

export function deleteExperiment(experimentId: number): DeleteExperimentAction {
    return {
      type: actionTypes.DELETE_EXPERIMENT,
      experimentId
    }
}
