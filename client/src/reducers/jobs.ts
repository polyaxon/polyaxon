import {Reducer} from "redux";
import * as _ from "lodash";

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
        byUuids: {...state.byUuids, [action.jobUuid]: {...state.byUuids[action.jobUuid], deleted: true}},
        uuids: state.uuids.filter(uuid => uuid != action.jobUuid),
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
  }
  return state;
};
