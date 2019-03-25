import { normalize } from 'normalizr';
import { Reducer } from 'redux';

import * as _ from 'lodash';

import { actionTypes, JobAction } from '../actions/jobs';
import { ACTIONS } from '../constants/actions';
import { JobSchema } from '../constants/schemas';
import { STOPPED } from '../constants/statuses';
import { ErrorEmptyState, ErrorSchema, processErrorById, processErrorGlobal } from '../models/errors';
import { JobModel, JobsEmptyState, JobStateSchema } from '../models/job';
import {
  LoadingIndicatorEmptyState,
  LoadingIndicatorSchema,
  processLoadingIndicatorById,
  processLoadingIndicatorGlobal
} from '../models/loadingIndicator';
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

export const LoadingIndicatorJobReducer: Reducer<LoadingIndicatorSchema> =
  (state: LoadingIndicatorSchema = LoadingIndicatorEmptyState, action: JobAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_JOB_REQUEST:
        return {
          ...state,
          jobs: processLoadingIndicatorById(state.jobs, action.jobName, true, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_JOB_ERROR:
      case actionTypes.UPDATE_JOB_SUCCESS:
        return {
          ...state,
          jobs: processLoadingIndicatorById(state.jobs, action.jobName, false, ACTIONS.UPDATE)
        };

      case actionTypes.GET_JOB_REQUEST:
        return {
          ...state,
          jobs: processLoadingIndicatorGlobal(
            processLoadingIndicatorById(state.jobs, action.jobName, true, ACTIONS.GET),
            false,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_JOB_ERROR:
      case actionTypes.GET_JOB_SUCCESS:
        return {
          ...state,
          jobs: processLoadingIndicatorById(state.jobs, action.jobName, false, ACTIONS.GET)
        };

      case actionTypes.DELETE_JOB_REQUEST:
        return {
          ...state,
          jobs: processLoadingIndicatorById(state.jobs, action.jobName, true, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_JOB_ERROR:
      case actionTypes.DELETE_JOB_SUCCESS:
        return {
          ...state,
          jobs: processLoadingIndicatorById(state.jobs, action.jobName, false, ACTIONS.DELETE)
        };

      case actionTypes.ARCHIVE_JOB_REQUEST:
        return {
          ...state,
          jobs: processLoadingIndicatorById(state.jobs, action.jobName, true, ACTIONS.ARCHIVE)
        };
      case actionTypes.ARCHIVE_JOB_ERROR:
      case actionTypes.ARCHIVE_JOB_SUCCESS:
        return {
          ...state,
          jobs: processLoadingIndicatorById(state.jobs, action.jobName, false, ACTIONS.ARCHIVE)
        };

      case actionTypes.RESTORE_JOB_REQUEST:
        return {
          ...state,
          jobs: processLoadingIndicatorById(state.jobs, action.jobName, true, ACTIONS.RESTORE)
        };
      case actionTypes.RESTORE_JOB_ERROR:
      case actionTypes.RESTORE_JOB_SUCCESS:
        return {
          ...state,
          jobs: processLoadingIndicatorById(state.jobs, action.jobName, false, ACTIONS.RESTORE)
        };

      case actionTypes.STOP_JOB_REQUEST:
        return {
          ...state,
          jobs: processLoadingIndicatorById(state.jobs, action.jobName, true, ACTIONS.STOP)
        };
      case actionTypes.STOP_JOB_ERROR:
      case actionTypes.STOP_JOB_SUCCESS:
        return {
          ...state,
          jobs: processLoadingIndicatorById(state.jobs, action.jobName, false, ACTIONS.STOP)
        };

      case actionTypes.BOOKMARK_JOB_REQUEST:
        return {
          ...state,
          jobs: processLoadingIndicatorById(state.jobs, action.jobName, true, ACTIONS.BOOKMARK)
        };
      case actionTypes.BOOKMARK_JOB_ERROR:
      case actionTypes.BOOKMARK_JOB_SUCCESS:
        return {
          ...state,
          jobs: processLoadingIndicatorById(state.jobs, action.jobName, false, ACTIONS.BOOKMARK)
        };

      case actionTypes.UNBOOKMARK_JOB_REQUEST:
        return {
          ...state,
          jobs: processLoadingIndicatorById(state.jobs, action.jobName, true, ACTIONS.UNBOOKMARK)
        };
      case actionTypes.UNBOOKMARK_JOB_ERROR:
      case actionTypes.UNBOOKMARK_JOB_SUCCESS:
        return {
          ...state,
          jobs: processLoadingIndicatorById(state.jobs, action.jobName, false, ACTIONS.UNBOOKMARK)
        };

      case actionTypes.FETCH_JOBS_REQUEST:
        return {
          ...state,
          jobs: processLoadingIndicatorGlobal(state.jobs, true, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_JOBS_ERROR:
      case actionTypes.FETCH_JOBS_SUCCESS:
        return {
          ...state,
          jobs: processLoadingIndicatorGlobal(state.jobs, false, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_JOB_REQUEST:
        return {
          ...state,
          jobs: processLoadingIndicatorGlobal(state.jobs, true, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_JOB_ERROR:
        return {
          ...state,
          jobs: processLoadingIndicatorGlobal(state.jobs, false, ACTIONS.CREATE)
        };
      default:
        return state;
    }
  };

export const ErrorJobReducer: Reducer<ErrorSchema> =
  (state: ErrorSchema = ErrorEmptyState, action: JobAction) => {
    switch (action.type) {
      case actionTypes.UPDATE_JOB_REQUEST:
      case actionTypes.UPDATE_JOB_SUCCESS:
        return {
          ...state,
          jobs: processErrorById(state.jobs, action.jobName, null, ACTIONS.UPDATE)
        };
      case actionTypes.UPDATE_JOB_ERROR:
        return {
          ...state,
          jobs: processErrorById(state.jobs, action.jobName, action.error, ACTIONS.UPDATE)
        };

      case actionTypes.GET_JOB_REQUEST:
      case actionTypes.GET_JOB_SUCCESS:
        return {
          ...state,
          jobs: processErrorGlobal(
            processErrorById(state.jobs, action.jobName, null, ACTIONS.GET),
            null,
            ACTIONS.CREATE)
        };
      case actionTypes.GET_JOB_ERROR:
        return {
          ...state,
          jobs: processErrorById(state.jobs, action.jobName, action.error, ACTIONS.GET)
        };

      case actionTypes.DELETE_JOB_REQUEST:
      case actionTypes.DELETE_JOB_SUCCESS:
        return {
          ...state,
          jobs: processErrorById(state.jobs, action.jobName, null, ACTIONS.DELETE)
        };
      case actionTypes.DELETE_JOB_ERROR:
        return {
          ...state,
          jobs: processErrorById(state.jobs, action.jobName, action.error, ACTIONS.DELETE)
        };

      case actionTypes.ARCHIVE_JOB_REQUEST:
      case actionTypes.ARCHIVE_JOB_SUCCESS:
        return {
          ...state,
          jobs: processErrorById(state.jobs, action.jobName, null, ACTIONS.ARCHIVE)
        };
      case actionTypes.ARCHIVE_JOB_ERROR:
        return {
          ...state,
          jobs: processErrorById(state.jobs, action.jobName, action.error, ACTIONS.ARCHIVE)
        };

      case actionTypes.RESTORE_JOB_REQUEST:
      case actionTypes.RESTORE_JOB_SUCCESS:
        return {
          ...state,
          jobs: processErrorById(state.jobs, action.jobName, null, ACTIONS.RESTORE)
        };
      case actionTypes.RESTORE_JOB_ERROR:
        return {
          ...state,
          jobs: processErrorById(state.jobs, action.jobName, action.error, ACTIONS.RESTORE)
        };

      case actionTypes.STOP_JOB_REQUEST:
      case actionTypes.STOP_JOB_SUCCESS:
        return {
          ...state,
          jobs: processErrorById(state.jobs, action.jobName, null, ACTIONS.STOP)
        };
      case actionTypes.STOP_JOB_ERROR:
        return {
          ...state,
          jobs: processErrorById(state.jobs, action.jobName, action.error, ACTIONS.STOP)
        };

      case actionTypes.BOOKMARK_JOB_REQUEST:
      case actionTypes.BOOKMARK_JOB_SUCCESS:
        return {
          ...state,
          jobs: processErrorById(state.jobs, action.jobName, null, ACTIONS.BOOKMARK)
        };
      case actionTypes.BOOKMARK_JOB_ERROR:
        return {
          ...state,
          jobs: processErrorById(state.jobs, action.jobName, action.error, ACTIONS.BOOKMARK)
        };

      case actionTypes.UNBOOKMARK_JOB_REQUEST:
      case actionTypes.UNBOOKMARK_JOB_SUCCESS:
        return {
          ...state,
          jobs: processErrorById(state.jobs, action.jobName, null, ACTIONS.UNBOOKMARK)
        };
      case actionTypes.UNBOOKMARK_JOB_ERROR:
        return {
          ...state,
          jobs: processErrorById(state.jobs, action.jobName, action.error, ACTIONS.UNBOOKMARK)
        };

      case actionTypes.FETCH_JOBS_REQUEST:
      case actionTypes.FETCH_JOBS_SUCCESS:
        return {
          ...state,
          jobs: processErrorGlobal(state.jobs, null, ACTIONS.FETCH)
        };
      case actionTypes.FETCH_JOBS_ERROR:
        return {
          ...state,
          jobs: processErrorGlobal(state.jobs, action.error, ACTIONS.FETCH)
        };

      case actionTypes.CREATE_JOB_REQUEST:
        return {
          ...state,
          jobs: processErrorGlobal(state.jobs, null, ACTIONS.CREATE)
        };
      case actionTypes.CREATE_JOB_ERROR:
        return {
          ...state,
          jobs: processErrorGlobal(state.jobs, action.error, ACTIONS.CREATE)
        };
      default:
        return state;
    }
  };
