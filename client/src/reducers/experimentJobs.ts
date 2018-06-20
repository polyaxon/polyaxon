import { Reducer } from 'redux';
import { normalize } from 'normalizr';

import * as _ from 'lodash';

import { JobSchema } from '../constants/schemas';
import { ExperimentJobAction, actionTypes } from '../actions/experimentJob';
import { ExperimentJobStateSchema, ExperimentJobsEmptyState, ExperimentJobModel } from '../models/experimentJob';
import { getExperimentIndexName, getExperimentJobIndexName } from '../constants/utils';
import { ExperimentsEmptyState, ExperimentStateSchema } from '../models/experiment';

export const ExperimentJobsReducer: Reducer<ExperimentJobStateSchema> =
  (state: ExperimentJobStateSchema = ExperimentJobsEmptyState, action: ExperimentJobAction) => {
    let newState = {...state};

    let processJob = function (experimentJob: ExperimentJobModel) {
      let uniqueName = getExperimentJobIndexName(experimentJob.unique_name);
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      let normalizedJobs = normalize(experimentJob, JobSchema).entities.jobs;
      newState.byUniqueNames[uniqueName] = {
        ...newState.byUniqueNames[uniqueName], ...normalizedJobs[experimentJob.unique_name]
      };
      return newState;
    };

    switch (action.type) {
      case actionTypes.CREATE_EXPERIMENT_JOB:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [getExperimentJobIndexName(action.job.unique_name)]: action.job
          },
          uniqueNames: [
            ...state.uniqueNames,
            getExperimentJobIndexName(action.job.unique_name)
          ]
        };
      case actionTypes.DELETE_EXPERIMENT_JOB:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames, [
              getExperimentJobIndexName(action.job.unique_name)]: {
              ...state.byUniqueNames[getExperimentJobIndexName(action.job.unique_name)],
              deleted: true
            }
          },
          uniqueNames: state.uniqueNames.filter(
            name => name !== getExperimentJobIndexName(action.job.unique_name)),
        };
      case actionTypes.UPDATE_EXPERIMENT_JOB:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [getExperimentJobIndexName(action.job.unique_name)]: action.job}
        };
      case actionTypes.RECEIVE_EXPERIMENT_JOBS:
        for (let job of action.jobs) {
          newState = processJob(job);
        }
        return newState;
      case actionTypes.RECEIVE_EXPERIMENT_JOB:
        return processJob(action.job);
      default:
        return state;
    }
  };

export const ExperimentJobExperimentsReducer: Reducer<ExperimentStateSchema> =
  (state: ExperimentStateSchema = ExperimentsEmptyState, action: ExperimentJobAction) => {
    let newState = {...state};

    let processJob = function (experimentJob: ExperimentJobModel) {
      let uniqueName = getExperimentJobIndexName(experimentJob.unique_name);
      let experimentName = getExperimentIndexName(experimentJob.experiment_name);
      if (_.includes(newState.uniqueNames, experimentName) &&
        !_.includes(newState.byUniqueNames[experimentName].jobs, uniqueName)) {
        newState.byUniqueNames[experimentName].jobs.push(uniqueName);
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.RECEIVE_EXPERIMENT_JOB:
        return processJob(action.job);
      case actionTypes.RECEIVE_EXPERIMENT_JOBS:
        for (let job of action.jobs) {
          newState = processJob(job);
        }
        return newState;
      default:
        return state;
    }
  };
