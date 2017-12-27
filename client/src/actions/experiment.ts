import {Action, Dispatch} from "redux";
import * as _ from "lodash";

import {ExperimentModel} from "../models/experiment";
import {EXPERIMENTS_URL, PROJECTS_URL} from "../constants/api";


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
  experimentUuid: string
}

export interface ReceiveExperimentsAction extends Action {
  type: actionTypes.RECEIVE_EXPERIMENTS;
  experiments: ExperimentModel[]
}

export interface RequestExperimentsAction extends Action {
  type: actionTypes.REQUEST_EXPERIMENTS;
}

export type ExperimentAction = CreateUpdateExperimentAction | DeleteExperimentAction | ReceiveExperimentsAction | RequestExperimentsAction;

export function createExperimentActionCreator(experiment: ExperimentModel): CreateUpdateExperimentAction {
    return {
      type: actionTypes.CREATE_EXPERIMENT,
      experiment
    }
}

export function updateExperimentActionCreator(experiment: ExperimentModel): CreateUpdateExperimentAction {
    return {
      type: actionTypes.UPDATE_EXPERIMENT,
      experiment
    }
}

export function deleteExperimentActionCreator(experimentUuid: string): DeleteExperimentAction {
    return {
      type: actionTypes.DELETE_EXPERIMENT,
      experimentUuid
    }
}

export function requestExperimentsActionCreator(): RequestExperimentsAction {
  return {
    type: actionTypes.REQUEST_EXPERIMENTS,
  }
}

export function receiveExperimentsActionCreator(experiments: ExperimentModel[]): ReceiveExperimentsAction {
  return {
    type: actionTypes.RECEIVE_EXPERIMENTS,
    experiments
  }
}

export function fetchExperiments(): Dispatch<ExperimentModel[]> {
  return (dispatch: any)=> {
    dispatch(requestExperimentsActionCreator());
    return fetch(EXPERIMENTS_URL, {
        headers: {
            'Authorization': 'token 8ff04973157b2a5831329fbb1befd37f93e4de4f'
        }
      })
      .then(response => response.json())
      .then(json => json.results.map((xp: {[key: string]: any})=> {
          return {
            ...xp,
            createdAt: new Date(_.toString(xp.created_at)),
            updatedAt: new Date(_.toString(xp.updated_at))};
        })
      )
      .then(json => dispatch(receiveExperimentsActionCreator(json)))
  }
}
