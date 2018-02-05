import { Reducer } from 'redux';
import { normalize } from 'normalizr';

import * as _ from 'lodash';

import { JobSchema } from '../constants/schemas';
import { JobAction, actionTypes } from '../actions/job';
import { JobStateSchema, JobsEmptyState } from '../models/job';
import { getJobIndexName } from '../constants/utils';

export const jobsReducer: Reducer<JobStateSchema> =
  (state: JobStateSchema = JobsEmptyState, action: JobAction) => {
    let newState = {...state};
    switch (action.type) {
      case actionTypes.CREATE_JOB:
        return {
          ...state,
          ByUniqueNames: {...state.ByUniqueNames, [getJobIndexName(action.job.unique_name)]: action.job},
          uniqueNames: [...state.uniqueNames, getJobIndexName(action.job.unique_name)]
        };
      case actionTypes.DELETE_JOB:
        return {
          ...state,
          ByUniqueNames: {
            ...state.ByUniqueNames,
            [getJobIndexName(action.job.unique_name)]: {
              ...state.ByUniqueNames[getJobIndexName(action.job.unique_name)], deleted: true}
          },
          uniqueNames: state.uniqueNames.filter(
            name => name !== getJobIndexName(action.job.unique_name)),
        };
      case actionTypes.UPDATE_JOB:
        return {
          ...state,
          ByUniqueNames: {...state.ByUniqueNames, [getJobIndexName(action.job.unique_name)]: action.job}
        };
      case actionTypes.RECEIVE_JOBS:
        for (let job of action.jobs) {
          let jobUniqueName = getJobIndexName(job.unique_name);
          if (!_.includes(newState.uniqueNames, jobUniqueName)) {
            newState.uniqueNames.push(jobUniqueName);
            newState.ByUniqueNames[jobUniqueName] = job;
          }
          newState.ByUniqueNames[jobUniqueName] = job;
        }
        return newState;
      case actionTypes.RECEIVE_JOB:
        let jobUniqueName = getJobIndexName(action.job.unique_name);
        if (!_.includes(newState.uniqueNames, jobUniqueName)) {
          newState.uniqueNames.push(jobUniqueName);
        }
        let normalizedJobs = normalize(action.job, JobSchema).entities.jobs;
        newState.ByUniqueNames[jobUniqueName] = normalizedJobs[action.job.unique_name];
        return newState;
    }
    return state;
  };
