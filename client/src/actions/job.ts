import {Action, Dispatch} from "redux";
import * as _ from "lodash";

import {urlifyProjectName, getStoredToken} from "../constants/utils"
import {JobModel} from "../models/job";
import {BASE_URL} from "../constants/api";


export enum actionTypes {
  CREATE_JOB='CREATE_JOB',
  DELETE_JOB='DELETE_JOB',
  UPDATE_JOB='UPDATE_JOB',
  RECEIVE_JOB='RECEIVE_JOB',
  RECEIVE_JOBS='RECEIVE_JOBS',
  REQUEST_JOB='REQUEST_JOB',
  REQUEST_JOBS='REQUEST_JOBS',
}

export interface CreateUpdateReceiveJobAction extends Action {
  type: actionTypes.CREATE_JOB | actionTypes.UPDATE_JOB | actionTypes.RECEIVE_JOB;
  job: JobModel
}

export interface DeleteJobAction extends Action {
  type: actionTypes.DELETE_JOB;
  job: JobModel
}

export interface ReceiveJobsAction extends Action {
  type: actionTypes.RECEIVE_JOBS;
  jobs: JobModel[]
}

export interface RequestJobsAction extends Action {
  type: actionTypes.REQUEST_JOBS | actionTypes.REQUEST_JOB;
}

export type JobAction = CreateUpdateReceiveJobAction | DeleteJobAction | ReceiveJobsAction | RequestJobsAction;

export function createJobActionCreator(job: JobModel): CreateUpdateReceiveJobAction {
    return {
      type: actionTypes.CREATE_JOB,
      job
    }
}

export function updateJobActionCreator(job: JobModel): CreateUpdateReceiveJobAction {
    return {
      type: actionTypes.UPDATE_JOB,
      job
    }
}

export function deleteJobActionCreator(job: JobModel): DeleteJobAction {
    return {
      type: actionTypes.DELETE_JOB,
      job
    }
}

export function requestJobActionCreator(): RequestJobsAction {
  return {
    type: actionTypes.REQUEST_JOB,
  }
}

export function requestJobsActionCreator(): RequestJobsAction {
  return {
    type: actionTypes.REQUEST_JOBS,
  }
}


export function receiveJobActionCreator(job: JobModel): CreateUpdateReceiveJobAction {
  return {
    type: actionTypes.RECEIVE_JOB,
    job
  }
}

export function receiveJobsActionCreator(jobs: JobModel[]): ReceiveJobsAction {
  return {
    type: actionTypes.RECEIVE_JOBS,
    jobs
  }
}

export function fetchJobs(projectUniqueName: string, experimentSequence: number): Dispatch<JobModel[]> {
  return (dispatch: any)=> {
    dispatch(requestJobsActionCreator());
    return fetch(BASE_URL + `/${urlifyProjectName(projectUniqueName)}` + '/experiments/' + experimentSequence + '/jobs', {
        headers: {
            'Authorization': 'token ' + getStoredToken()
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
      .then(json => dispatch(receiveJobsActionCreator(json)))
  }
}

export function fetchJob(user: string, projectName: string, experimentSequence: number, jobSequence: number): Dispatch<JobModel> {
  return (dispatch: any) => {
    dispatch(requestJobActionCreator());
    return fetch(BASE_URL + `/${user}/${projectName}` + '/experiments/' + experimentSequence + '/jobs/' + jobSequence, {
        headers: {
            'Authorization': 'token ' + getStoredToken()
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
      .then(json => dispatch(receiveJobActionCreator(json)))
  }
}

