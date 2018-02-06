import { Reducer } from 'redux';
import { normalize } from 'normalizr';

import * as _ from 'lodash';

import { JobSchema } from '../constants/schemas';
import { JobAction, actionTypes } from '../actions/job';
import { JobStateSchema, JobsEmptyState, JobModel } from '../models/job';
import { getExperimentIndexName, getJobIndexName } from '../constants/utils';
import { ExperimentsEmptyState, ExperimentStateSchema } from '../models/experiment';

export const jobsReducer: Reducer<JobStateSchema> =
  (state: JobStateSchema = JobsEmptyState, action: JobAction) => {
    let newState = {...state};

    let processJob = function (job: JobModel) {
      let uniqueName = getJobIndexName(job.unique_name);
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      let normalizedJobs = normalize(job, JobSchema).entities.jobs;
      newState.byUniqueNames[uniqueName] = {
        ...newState.byUniqueNames[uniqueName], ...normalizedJobs[job.unique_name]
      };
      return newState;
    };

    switch (action.type) {
      case actionTypes.CREATE_JOB:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [getJobIndexName(action.job.unique_name)]: action.job},
          uniqueNames: [...state.uniqueNames, getJobIndexName(action.job.unique_name)]
        };
      case actionTypes.DELETE_JOB:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [getJobIndexName(action.job.unique_name)]: {
              ...state.byUniqueNames[getJobIndexName(action.job.unique_name)], deleted: true}
          },
          uniqueNames: state.uniqueNames.filter(
            name => name !== getJobIndexName(action.job.unique_name)),
        };
      case actionTypes.UPDATE_JOB:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [getJobIndexName(action.job.unique_name)]: action.job}
        };
      case actionTypes.RECEIVE_JOBS:
        for (let job of action.jobs) {
          newState = processJob(job);
        }
        return newState;
      case actionTypes.RECEIVE_JOB:
        return processJob(action.job);
      default:
        return state;
    }
  };

export const ExperimentJobsReducer: Reducer<ExperimentStateSchema> =
  (state: ExperimentStateSchema = ExperimentsEmptyState, action: JobAction) => {
    let newState = {...state};

    let processJob = function (job: JobModel) {
      let uniqueName = getJobIndexName(job.unique_name);
      let experimentName = getExperimentIndexName(job.experiment_name);
      if (_.includes(newState.uniqueNames, experimentName) &&
        !_.includes(newState.byUniqueNames[experimentName].jobs, uniqueName)) {
        newState.byUniqueNames[experimentName].jobs.push(uniqueName);
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.RECEIVE_JOB:
        return processJob(action.job);
      case actionTypes.RECEIVE_JOBS:
        for (let job of action.jobs) {
          newState = processJob(job);
        }
        return newState;
      default:
        return state;
    }
  };
