import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, ExperimentJobAction } from '../actions/experimentJobs';
import { ACTIONS } from '../constants/actions';
import { JobSchema } from '../constants/schemas';
import { getExperimentIndexName, getExperimentJobIndexName } from '../constants/utils';
import { AlertEmptyState, AlertSchema, processErrorById, processErrorGlobal } from '../models/alerts';
import { ExperimentsEmptyState, ExperimentStateSchema } from '../models/experiment';
import { ExperimentJobModel, ExperimentJobsEmptyState, ExperimentJobStateSchema } from '../models/experimentJob';
import {
  LoadingIndicatorEmptyState,
  LoadingIndicatorSchema,
  processLoadingIndicatorById,
  processLoadingIndicatorGlobal
} from '../models/loadingIndicator';
import { LastFetchedNames } from '../models/utils';

export const ExperimentJobsReducer: Reducer<ExperimentJobStateSchema> =
  (state: ExperimentJobStateSchema = ExperimentJobsEmptyState, action: ExperimentJobAction) => {
    let newState = {...state};

    const processJob = (experimentJob: ExperimentJobModel) => {
      const uniqueName = getExperimentJobIndexName(experimentJob.unique_name);
      if (!_.includes(newState.lastFetched.names, uniqueName)) {
        newState.lastFetched.names.push(uniqueName);
      }
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      const normalizedJobs = normalize(experimentJob, JobSchema).entities.jobs;
      newState.byUniqueNames[uniqueName] = {
        ...newState.byUniqueNames[uniqueName], ...normalizedJobs[experimentJob.unique_name]
      };
      return newState;
    };

    switch (action.type) {
      case actionTypes.FETCH_EXPERIMENT_JOBS_REQUEST:
        newState.lastFetched = new LastFetchedNames();
        return newState;
      case actionTypes.FETCH_EXPERIMENT_JOBS_SUCCESS:
        newState.lastFetched = new LastFetchedNames();
        newState.lastFetched.count = action.count;
        for (const job of action.jobs) {
          newState = processJob(job);
        }
        return newState;
      case actionTypes.GET_EXPERIMENT_JOB_SUCCESS:
        newState = processJob(action.job);
        newState.lastFetched.count += 1;
        return newState;
      default:
        return state;
    }
  };

export const ExperimentJobExperimentsReducer: Reducer<ExperimentStateSchema> =
  (state: ExperimentStateSchema = ExperimentsEmptyState, action: ExperimentJobAction) => {
    let newState = {...state};

    const processJob = function (experimentJob: ExperimentJobModel) {
      const uniqueName = getExperimentJobIndexName(experimentJob.unique_name);
      const experimentName = getExperimentIndexName(uniqueName, true);
      if (_.includes(newState.uniqueNames, experimentName) &&
        !_.includes(newState.byUniqueNames[experimentName].jobs, uniqueName)) {
        newState.byUniqueNames[experimentName].jobs.push(uniqueName);
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.GET_EXPERIMENT_JOB_SUCCESS:
        return processJob(action.job);
      case actionTypes.FETCH_EXPERIMENT_JOBS_SUCCESS:
        for (const job of action.jobs) {
          newState = processJob(job);
        }
        return newState;
      default:
        return state;
    }
  };

export const LoadingIndicatorExperimentJobReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: ExperimentJobAction) => {
    switch (action.type) {
      case actionTypes.GET_EXPERIMENT_JOB_REQUEST:
        return {
          ...state,
          experimentJobs: processLoadingIndicatorGlobal(
            processLoadingIndicatorById(state.experimentJobs, action.jobName, true, ACTIONS.GET),
            false,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_EXPERIMENT_JOB_ERROR:
      case actionTypes.GET_EXPERIMENT_JOB_SUCCESS:
        return {
          ...state,
          experimentJobs: processLoadingIndicatorById(state.experimentJobs, action.jobName, false, ACTIONS.GET)
        };

      case actionTypes.FETCH_EXPERIMENT_JOBS_REQUEST:
        return {
          ...state,
          experimentJobs: processLoadingIndicatorGlobal(state.experimentJobs, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_EXPERIMENT_JOBS_ERROR:
      case actionTypes.FETCH_EXPERIMENT_JOBS_SUCCESS:
        return {
          ...state,
          experimentJobs: processLoadingIndicatorGlobal(state.experimentJobs, false, ACTIONS.FETCH)
        };
      default:
        return state;
    }
  };

export const AlertExperimentJobReducer: Reducer<AlertSchema> =
  (state: AlertSchema = AlertEmptyState, action: ExperimentJobAction) => {
    switch (action.type) {
      case actionTypes.GET_EXPERIMENT_JOB_REQUEST:
        return {
          ...state,
          experimentJobs: processErrorGlobal(
            processErrorById(state.experimentJobs, action.jobName, null, null, ACTIONS.GET),
            null,
            null,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_EXPERIMENT_JOB_SUCCESS:
        return {
          ...state,
          experimentJobs: processErrorById(state.experimentJobs, action.jobName, null , true, ACTIONS.GET)
        };
      case actionTypes.GET_EXPERIMENT_JOB_ERROR:
        return {
          ...state,
          experimentJobs: processErrorById(state.experimentJobs, action.jobName, action.error, false, ACTIONS.GET)
        };

      case actionTypes.FETCH_EXPERIMENT_JOBS_REQUEST:
        return {
          ...state,
          experimentJobs: processErrorGlobal(state.experimentJobs, null, null, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_EXPERIMENT_JOBS_SUCCESS:
        return {
          ...state,
          experimentJobs: processErrorGlobal(state.experimentJobs, null, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_EXPERIMENT_JOBS_ERROR:
        return {
          ...state,
          experimentJobs: processErrorGlobal(state.experimentJobs, action.error, false, ACTIONS.FETCH)
        };
      default:
        return state;
    }
  };
