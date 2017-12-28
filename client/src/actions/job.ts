import {Action, Dispatch} from "redux";
import * as _ from "lodash";

import {urlifyProjectName} from "../constants/utils"
import {JobModel} from "../models/job";
import {BASE_URL} from "../constants/api";


export enum actionTypes {
  CREATE_JOB='CREATE_JOB',
  DELETE_JOB='DELETE_JOB',
  UPDATE_JOB='UPDATE_JOB',
  RECEIVE_JOBS='RECEIVE_JOBS',
  REQUEST_JOBS='REQUEST_JOBS',
}

export interface CreateUpdateJobAction extends Action {
  type: actionTypes.CREATE_JOB | actionTypes.UPDATE_JOB;
  job: JobModel
}

export interface DeleteJobAction extends Action {
  type: actionTypes.DELETE_JOB;
  jobUuid: string
}

export interface ReceiveJobsAction extends Action {
  type: actionTypes.RECEIVE_JOBS;
  jobs: JobModel[]
}

export interface RequestJobsAction extends Action {
  type: actionTypes.REQUEST_JOBS;
}

export type JobAction = CreateUpdateJobAction | DeleteJobAction | ReceiveJobsAction | RequestJobsAction;

export function createJobActionCreator(job: JobModel): CreateUpdateJobAction {
    return {
      type: actionTypes.CREATE_JOB,
      job
    }
}

export function updateJobActionCreator(job: JobModel): CreateUpdateJobAction {
    return {
      type: actionTypes.UPDATE_JOB,
      job
    }
}

export function deleteJobActionCreator(jobUuid: string): DeleteJobAction {
    return {
      type: actionTypes.DELETE_JOB,
      jobUuid
    }
}

export function requestJobsActionCreator(): RequestJobsAction {
  return {
    type: actionTypes.REQUEST_JOBS,
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
      .then(json => dispatch(receiveJobsActionCreator(json)))
  }
}
