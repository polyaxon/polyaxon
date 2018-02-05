import { Reducer } from 'redux';
import { normalize } from 'normalizr';

import * as _ from 'lodash';

import { JobSchema } from '../constants/schemas';
import { JobAction, actionTypes } from '../actions/job';
import { JobStateSchema, JobsEmptyState } from '../models/job';

export const jobsReducer: Reducer<JobStateSchema> =
  (state: JobStateSchema = JobsEmptyState, action: JobAction) => {
    let newState = {...state};
    switch (action.type) {
      case actionTypes.CREATE_JOB:
        return {
          ...state,
          ByUniqueNames: {...state.ByUniqueNames, [action.job.unique_name]: action.job},
          uniqueNames: [...state.uniqueNames, action.job.unique_name]
        };
      case actionTypes.DELETE_JOB:
        return {
          ...state,
          ByUniqueNames: {
            ...state.ByUniqueNames,
            [action.job.sequence]: {...state.ByUniqueNames[action.job.unique_name], deleted: true}
          },
          uniqueNames: state.uniqueNames.filter(
            name => name !== action.job.unique_name),
        };
      case actionTypes.UPDATE_JOB:
        return {
          ...state,
          ByUniqueNames: {...state.ByUniqueNames, [action.job.unique_name]: action.job}
        };
      case actionTypes.RECEIVE_JOBS:
        for (let xp of action.jobs) {
          if (!_.includes(newState.uniqueNames, xp.unique_name)) {
            newState.uniqueNames.push(xp.unique_name);
            newState.ByUniqueNames[xp.unique_name] = xp;
          }
          newState.ByUniqueNames[xp.unique_name] = xp;
        }
        return newState;
      case actionTypes.RECEIVE_JOB:
        let uniqueName = action.job.unique_name;
        if (!_.includes(newState.uniqueNames, uniqueName)) {
          newState.uniqueNames.push(uniqueName);
        }
        let normalizedJobs = normalize(action.job, JobSchema).entities.jobs;
        newState.ByUniqueNames[uniqueName] = normalizedJobs[uniqueName];
        return newState;
    }
    return state;
  };
