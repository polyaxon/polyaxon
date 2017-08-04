import {Action, Dispatch} from "redux";

import {ExperimentModel} from "../models/experiment";
import {EXPERIMENTS_URL} from "../constants/api";


export enum actionTypes {
  CREATE_EXPERIMENT='CREATE_EXPERIMENT',
  DELETE_EXPERIMENT='DELETE_EXPERIMENT',
  UPDATE_EXPERIMENT='UPDATE_EXPERIMENT',
  RECEIVE_EXPERIMENTS='RECEIVE_EXPERIMENTS',
  REQUEST_EXPERIMENTS='REQUEST_EXPERIMENTS',
}

export interface CreateUpdateExperimentAction extends Action {
  type: actionTypes.CREATE_EXPERIMENT | actionTypes.UPDATE_EXPERIMENT;
  experiment: ExperimentModel
}

export interface DeleteExperimentAction extends Action {
  type: actionTypes.DELETE_EXPERIMENT;
  experimentId: number
}

export interface ReceiveExperiments extends Action {
  type: actionTypes.RECEIVE_EXPERIMENTS;
  experiments: ExperimentModel[]
}

export interface RequestExperiments extends Action {
  type: actionTypes.REQUEST_EXPERIMENTS;
}

export type ExperimentAction = CreateUpdateExperimentAction | DeleteExperimentAction | ReceiveExperiments | RequestExperiments;

export function createExperiment(experiment: ExperimentModel): CreateUpdateExperimentAction {
    return {
      type: actionTypes.CREATE_EXPERIMENT,
      experiment
    }
}

export function updateExperiment(experiment: ExperimentModel): CreateUpdateExperimentAction {
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

export function requestExperiments(): RequestExperiments {
  return {
    type: actionTypes.REQUEST_EXPERIMENTS,
  }
}

export function receiveExperiments(experiments: ExperimentModel[]): ReceiveExperiments {
  return {
    type: actionTypes.RECEIVE_EXPERIMENTS,
    experiments
  }
}

export function fetchExperiments(): Dispatch<ExperimentModel[]> {
  return dispatch => {
    dispatch(requestExperiments());
    return fetch(EXPERIMENTS_URL)
      .then(response => response.json())
      .then(json => dispatch(receiveExperiments(json)))
  }
}
