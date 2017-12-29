import {Action, Dispatch} from "redux";
import * as _ from "lodash";

import {urlifyProjectName} from "../constants/utils"
import {ExperimentModel} from "../models/experiment";
import {BASE_URL} from "../constants/api";


export enum actionTypes {
  CREATE_EXPERIMENT='CREATE_EXPERIMENT',
  DELETE_EXPERIMENT='DELETE_EXPERIMENT',
  UPDATE_EXPERIMENT='UPDATE_EXPERIMENT',
  RECEIVE_EXPERIMENT='RECEIVE_EXPERIMENT',
  RECEIVE_EXPERIMENTS='RECEIVE_EXPERIMENTS',
  REQUEST_EXPERIMENTS='REQUEST_EXPERIMENTS',
}

export interface CreateUpdateReceiveExperimentAction extends Action {
  type: actionTypes.CREATE_EXPERIMENT | actionTypes.UPDATE_EXPERIMENT | actionTypes.RECEIVE_EXPERIMENT;
  experiment: ExperimentModel
}

export interface DeleteExperimentAction extends Action {
  type: actionTypes.DELETE_EXPERIMENT;
  experiment: ExperimentModel
}

export interface ReceiveExperimentsAction extends Action {
  type: actionTypes.RECEIVE_EXPERIMENTS;
  experiments: ExperimentModel[]
}

export interface RequestExperimentsAction extends Action {
  type: actionTypes.REQUEST_EXPERIMENTS;
}

export type ExperimentAction = CreateUpdateReceiveExperimentAction | DeleteExperimentAction | ReceiveExperimentsAction | RequestExperimentsAction;

export function createExperimentActionCreator(experiment: ExperimentModel): CreateUpdateReceiveExperimentAction {
    return {
      type: actionTypes.CREATE_EXPERIMENT,
      experiment
    }
}

export function updateExperimentActionCreator(experiment: ExperimentModel): CreateUpdateReceiveExperimentAction {
    return {
      type: actionTypes.UPDATE_EXPERIMENT,
      experiment
    }
}

export function deleteExperimentActionCreator(experiment: ExperimentModel): DeleteExperimentAction {
    return {
      type: actionTypes.DELETE_EXPERIMENT,
      experiment
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
  
export function receiveExperimentActionCreator(experiment: ExperimentModel): CreateUpdateReceiveExperimentAction {
  return {
    type: actionTypes.RECEIVE_EXPERIMENT,
    experiment
  }
}

export function fetchExperiments(projectUniqueName: string): Dispatch<ExperimentModel[]> {
  return (dispatch: any)=> {
    dispatch(requestExperimentsActionCreator());
    return fetch(BASE_URL + `/${urlifyProjectName(projectUniqueName)}` + '/experiments', {
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

export function fetchExperiment(user: string, projectName: string, experimentSequence: number): Dispatch<ExperimentModel> {
  return (dispatch: any) => {
    dispatch(requestExperimentsActionCreator());
    return fetch(BASE_URL + `/${user}` + `/${projectName}` + `/experiments/` + `${experimentSequence}`, {
        headers: {
            'Authorization': 'token 8ff04973157b2a5831329fbb1befd37f93e4de4f'
        }
    })
      .then(response => response.json())
      .then(json => {
          return {
            ...json,
            createdAt: new Date(_.toString(json.created_at)),
            updatedAt: new Date(_.toString(json.updated_at))};
        }
      )
      .then(json => dispatch(receiveExperimentActionCreator(json)))
  }
}

