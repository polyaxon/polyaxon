import { Action, combineReducers } from 'redux';
// import {reducer as formReducer } from 'redux-form';

import { projectsReducer, UserProjectsReducer } from './projects';
import { experimentsReducer, GroupExperimentsReducer, ProjectExperimentsReducer } from './experiments';
import { groupsReducer, ProjectGroupsReducer } from './groups';
import { jobsReducer } from './jobs';
import { ExperimentJobsReducer, ExperimentJobExperimentsReducer } from './experimentJobs';

import { tokenReducer } from './token';
import { AppState } from '../constants/types';
import { modalReducer } from './modal';
import { userReducer } from './user';
import { PaginationReducer } from './pagination';
import { logsReducer } from './logs';
import { buildsReducer } from './builds';

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
  pagination: PaginationReducer,
  logs: logsReducer
});

function SliceReducer(state: AppState, action: Action) {
  return {
    projects: ProjectGroupsReducer(ProjectExperimentsReducer(state.projects, action), action),
    groups: GroupExperimentsReducer(state.groups, action),
    experiments: ExperimentJobExperimentsReducer(state.experiments, action),
    jobs: state.jobs,
    builds: state.builds,
    experimentJobs: state.experimentJobs,
    modal: state.modal,
    auth: state.auth,
    users: UserProjectsReducer(state.users, action),
    // form: state.form,
    pagination: state.pagination,
    logs: state.logs
  };
}

function appReducer(state: AppState, action: Action) {
  let _state = combinedReducer(state, action);
  _state = SliceReducer(_state, action);
  return _state;
}

export default appReducer;
