///<reference path="statuses.ts"/>
import { Action, combineReducers } from 'redux';
// import {reducer as formReducer } from 'redux-form';

import { projectsReducer, UserProjectsReducer } from './projects';
import { experimentsReducer, GroupExperimentsReducer, ProjectExperimentsReducer } from './experiments';
import { groupsReducer, ProjectGroupsReducer } from './groups';
import { jobsReducer, ProjectJobsReducer } from './jobs';
import { ExperimentJobsReducer, ExperimentJobExperimentsReducer } from './experimentJobs';

import { tokenReducer } from './token';
import { AppState } from '../constants/types';
import { modalReducer } from './modal';
import { userReducer } from './user';
import { logsReducer } from './logs';
import { buildsReducer, ProjectBuildsReducer } from './builds';
import { StatusesReducer } from './statuses';
import { MetricsReducer } from './metrics';

const combinedReducer = combineReducers<AppState>({
  projects: projectsReducer,
  experiments: experimentsReducer,
  groups: groupsReducer,
  jobs: jobsReducer,
  builds: buildsReducer,
  experimentJobs: ExperimentJobsReducer,
  modal: modalReducer,
  auth: tokenReducer,
  users: userReducer,
  // form: formReducer,
  logs: logsReducer,
  statuses: StatusesReducer,
  metrics: MetricsReducer,
});

function SliceReducer(state: AppState, action: Action) {
  return {
    projects: ProjectGroupsReducer(
      ProjectExperimentsReducer(
        ProjectJobsReducer(
          ProjectBuildsReducer(
            state.projects,
            action),
          action),
        action),
      action),
    groups: GroupExperimentsReducer(state.groups, action),
    experiments: ExperimentJobExperimentsReducer(state.experiments, action),
    jobs: state.jobs,
    builds: state.builds,
    experimentJobs: state.experimentJobs,
    modal: state.modal,
    auth: state.auth,
    users: UserProjectsReducer(state.users, action),
    // form: state.form,
    logs: state.logs,
    statuses: state.statuses,
    metrics: state.metrics,
  };
}

function appReducer(state: AppState, action: Action) {
  let _state = combinedReducer(state, action);
  _state = SliceReducer(_state, action);
  return _state;
}

export default appReducer;
