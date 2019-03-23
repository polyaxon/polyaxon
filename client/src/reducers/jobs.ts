import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, JobAction } from '../actions/jobs';
import { JobSchema } from '../constants/schemas';
import { STOPPED } from '../constants/statuses';
import { JobModel, JobsEmptyState, JobStateSchema } from '../models/job';
import { ProjectsEmptyState, ProjectStateSchema } from '../models/project';
import { LastFetchedNames } from '../models/utils';

export const jobsReducer: Reducer<JobStateSchema> =
  (state: JobStateSchema = JobsEmptyState, action: JobAction) => {
    let newState = {...state};

    const processJob = (job: JobModel) => {
      const uniqueName = job.unique_name;
      if (!_.includes(newState.lastFetched.names, uniqueName)) {
        newState.lastFetched.names.push(uniqueName);
      }
      if (!_.includes(newState.uniqueNames, uniqueName)) {
        newState.uniqueNames.push(uniqueName);
      }
      if (_.isNil(job.deleted)) {
        job.deleted = false;
      }
      const normalizedJobs = normalize(job, JobSchema).entities.jobs;
      newState.byUniqueNames[uniqueName] = {
        ...newState.byUniqueNames[uniqueName], ...normalizedJobs[job.unique_name]
      };
      return newState;
    };

    switch (action.type) {
      case actionTypes.DELETE_JOB_SUCCESS:
        return {
          ...state,
          uniqueNames: state.uniqueNames.filter(
            (name) => name !== action.jobName),
          lastFetched: {
            ...state.lastFetched,
            names: state.lastFetched.names.filter((name) => name !== action.jobName)
          },
        };
      case actionTypes.ARCHIVE_JOB_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.jobName]: {
              ...state.byUniqueNames[action.jobName], deleted: true
            }
          },
        };
      case actionTypes.RESTORE_JOB_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.jobName]: {
              ...state.byUniqueNames[action.jobName], deleted: false
            }
          },
        };
      case actionTypes.STOP_JOB_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.jobName]: {
              ...state.byUniqueNames[action.jobName], last_status: STOPPED
            }
          },
        };
      case actionTypes.BOOKMARK_JOB_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.jobName]: {
              ...state.byUniqueNames[action.jobName], bookmarked: true
            }
          },
        };
      case actionTypes.UNBOOKMARK_JOB_SUCCESS:
        return {
          ...state,
          byUniqueNames: {
            ...state.byUniqueNames,
            [action.jobName]: {
              ...state.byUniqueNames[action.jobName], bookmarked: false
            }
          },
        };
      case actionTypes.UPDATE_JOB_SUCCESS:
        return {
          ...state,
          byUniqueNames: {...state.byUniqueNames, [action.job.unique_name]: action.job}
        };

      case actionTypes.FETCH_JOBS_REQUEST:
        newState.lastFetched = new LastFetchedNames();
        return newState;
      case actionTypes.FETCH_JOBS_SUCCESS:
        newState.lastFetched = new LastFetchedNames();
        newState.lastFetched.count = action.count;
        for (const job of action.jobs) {
          newState = processJob(job);
        }
        return newState;
      case actionTypes.GET_JOB_SUCCESS:
        return processJob(action.job);
      default:
        return state;
    }
  };

export const ProjectJobsReducer: Reducer<ProjectStateSchema> =
  (state: ProjectStateSchema = ProjectsEmptyState, action: JobAction) => {
    let newState = {...state};

    const processJob = (job: JobModel) => {
      const uniqueName = job.unique_name;
      const projectName = job.project;
      if (_.includes(newState.uniqueNames, projectName) &&
        !_.includes(newState.byUniqueNames[projectName].jobs, uniqueName)) {
        newState.byUniqueNames[projectName].jobs.push(uniqueName);
      }
      return newState;
    };

    switch (action.type) {
      case actionTypes.GET_JOB_SUCCESS:
        return processJob(action.job);
      case actionTypes.FETCH_JOBS_SUCCESS:
        for (const job of action.jobs) {
          newState = processJob(job);
        }
        return newState;
      default:
        return state;
    }
  };
