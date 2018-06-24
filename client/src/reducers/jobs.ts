import { Reducer } from 'redux';
import { normalize } from 'normalizr';

import * as _ from 'lodash';

import { JobSchema } from '../constants/schemas';
import { JobAction, actionTypes } from '../actions/job';
import { JobStateSchema, JobsEmptyState, JobModel } from '../models/job';
import { ProjectsEmptyState, ProjectStateSchema } from '../models/project';
import { LastFetched } from '../models/utils';

export const jobsReducer: Reducer<JobStateSchema> =
  (state: JobStateSchema = JobsEmptyState, action: JobAction) => {
    let newState = {...state};

    let processJob = function (job: JobModel) {
      let uniqueName = job.unique_name;
      newState.lastFetched.names.push(uniqueName);
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
          byUniqueNames: {...state.byUniqueNames, [action.job.unique_name]: action.job},
          uniqueNames: [...state.uniqueNames, action.job.unique_name]
        };
      case actionTypes.DELETE_JOB:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.job.unique_name]: {
              ...state.byUniqueNames[action.job.unique_name], deleted: true}
          },
          uniqueNames: state.uniqueNames.filter(
            name => name !== action.job.unique_name),
        };
      case actionTypes.UPDATE_JOB:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.job.unique_name]: action.job}
        };

      case actionTypes.REQUEST_JOBS:
        newState.lastFetched = new LastFetched();
        return newState;
      case actionTypes.RECEIVE_JOBS:
        newState.lastFetched = new LastFetched();
        newState.lastFetched.count = action.count;
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

export const ProjectJobsReducer: Reducer<ProjectStateSchema> =
  (state: ProjectStateSchema = ProjectsEmptyState, action: JobAction) => {
    let newState = {...state};

    let processJob = function (job: JobModel) {
      let uniqueName = job.unique_name;
      let projectName = job.project;
      if (_.includes(newState.uniqueNames, projectName) &&
        !_.includes(newState.byUniqueNames[projectName].jobs, uniqueName)) {
        newState.byUniqueNames[projectName].jobs.push(uniqueName);
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
