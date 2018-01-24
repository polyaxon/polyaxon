import {Reducer} from "redux";
import {normalize} from 'normalizr';

import * as _ from "lodash";

import {JobSchema} from "../constants/schemas"
import {JobAction, actionTypes} from "../actions/job";
import {JobStateSchema, JobsEmptyState} from "../models/job";

export const jobsReducer: Reducer<JobStateSchema> =
  (state: JobStateSchema = JobsEmptyState, action: JobAction) => {

    switch (action.type) {
      case actionTypes.CREATE_JOB:
        return {
          ...state,
          byUuids: {...state.byUuids, [action.job.uuid]: action.job},
          uuids: [...state.uuids, action.job.uuid]
        };
      case actionTypes.DELETE_JOB:
        return {
          ...state,
          byUuids: {
            ...state.byUuids,
            [action.job.sequence]: {...state.byUuids[action.job.uuid], deleted: true}
          },
          uuids: state.uuids.filter(uuid => uuid != action.job.uuid),
        };
      case actionTypes.UPDATE_JOB:
        return {
          ...state,
          byUuids: {...state.byUuids, [action.job.uuid]: action.job}
        };
      case actionTypes.RECEIVE_JOBS:
        var newState = {...state};
        for (let xp of action.jobs) {
          if (!_.includes(newState.uuids, xp.uuid)) {
            newState.uuids.push(xp.uuid);
            newState.byUuids[xp.uuid] = xp;
          }
          newState.byUuids[xp.uuid] = xp;
        }
        return newState;
      case actionTypes.RECEIVE_JOB:
        var newState = {...state};
        if (!_.includes(newState.uuids, action.job.uuid)) {
          newState.uuids.push(action.job.uuid);
        }
        let normalized_jobs = normalize(action.job, JobSchema).entities.jobs;
        newState.byUuids[action.job.uuid] = normalized_jobs[action.job.uuid];
        return newState;
    }
    return state;
  };
