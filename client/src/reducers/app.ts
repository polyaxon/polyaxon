import { Action, combineReducers } from 'redux';
import {reducer as formReducer } from 'redux-form';

import { projectsReducer } from './projects';
import { experimentsReducer, GroupExperimentsReducer, ProjectExperimentsReducer } from './experiments';
import { groupsReducer, ProjectGroupsReducer } from './groups';
import { ExperimentJobsReducer, jobsReducer } from './jobs';

import { tokenReducer } from './token';
import { AppState } from '../constants/types';
import { modalReducer } from '../reducers/modal';
import { userReducer } from '../reducers/user';
import { PaginationReducer } from '../reducers/pagination';

const combinedReducer = combineReducers<AppState>({
  projects: projectsReducer,
  experiments: experimentsReducer,
  groups: groupsReducer,
  jobs: jobsReducer,
  modal: modalReducer,
  auth: tokenReducer,
  user: userReducer,
  form: formReducer,
  pagination: PaginationReducer
});

function SliceReducer(state: AppState, action: Action) {
  return {
    projects: ProjectGroupsReducer(ProjectExperimentsReducer(state.projects, action), action),
    groups: GroupExperimentsReducer(state.groups, action),
    experiments: ExperimentJobsReducer(state.experiments, action),
    jobs: state.jobs,
    modal: state.modal,
    auth: state.auth,
    user: state.user,
    form: state.form,
    pagination: state.pagination
  };
}

function appReducer(state: AppState, action: Action) {
  let _state = combinedReducer(state, action);
  _state = SliceReducer(_state, action);
  return _state;
}

export default appReducer;
