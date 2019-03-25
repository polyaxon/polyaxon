import { Action, combineReducers } from 'redux';

import { ExperimentJobExperimentsReducer, ExperimentJobsReducer } from './experimentJobs';
import {
  ExperimentsParamsReducer,
  experimentsReducer,
  GroupExperimentsReducer,
  ProjectExperimentsReducer
} from './experiments';
import { groupsReducer, ProjectGroupsReducer } from './groups';
import { jobsReducer, ProjectJobsReducer } from './jobs';
import { projectsReducer, UserProjectsReducer } from './projects';

import { AppState } from '../constants/types';
import { activityLogsReducer } from './activityLogs';
import { buildsReducer, ProjectBuildsReducer } from './builds';
import { chartViewsReducer } from './chartViews';
import { codeReferencesReducer } from './codeReferences';
import { healthStatusReducer } from './healthStatus';
import { LoadingIndicatorReducer, LoadingIndicatorSliceReducer } from './loadingIndicator';
import { logsReducer } from './logs';
import { MetricsReducer } from './metrics';
import { modalReducer } from './modal';
import { notebooksReducer } from './notebooks';
import { outputsReducer } from './outputs';
import { searchesReducer } from './searches';
import { StatusesReducer } from './statuses';
import { tensorboardsReducer } from './tensorboards';
import { tokenReducer } from './token';
import { userReducer } from './user';

const combinedReducer = combineReducers<AppState>({
  projects: projectsReducer,
  experiments: experimentsReducer,
  experimentsParams: ExperimentsParamsReducer,
  groups: groupsReducer,
  jobs: jobsReducer,
  builds: buildsReducer,
  tensorboards: tensorboardsReducer,
  notebooks: notebooksReducer,
  experimentJobs: ExperimentJobsReducer,
  modal: modalReducer,
  auth: tokenReducer,
  healthStatus: healthStatusReducer,
  users: userReducer,
  // form: formReducer,
  logs: logsReducer,
  outputs: outputsReducer,
  statuses: StatusesReducer,
  metrics: MetricsReducer,
  activityLogs: activityLogsReducer,
  searches: searchesReducer,
  chartViews: chartViewsReducer,
  codeReferences: codeReferencesReducer,
  loadingIndicators: LoadingIndicatorReducer
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
    experimentsParams: state.experimentsParams,
    jobs: state.jobs,
    builds: state.builds,
    tensorboards: state.tensorboards,
    notebooks: state.notebooks,
    experimentJobs: state.experimentJobs,
    modal: state.modal,
    auth: state.auth,
    healthStatus: state.healthStatus,
    users: UserProjectsReducer(state.users, action),
    logs: state.logs,
    outputs: state.outputs,
    statuses: state.statuses,
    metrics: state.metrics,
    activityLogs: state.activityLogs,
    searches: state.searches,
    chartViews: state.chartViews,
    codeReferences: state.codeReferences,
    loadingIndicators: LoadingIndicatorSliceReducer(state, action),
  };
}

function appReducer(state: AppState, action: Action) {
  let _state = combinedReducer(state, action);
  _state = SliceReducer(_state, action);
  return _state;
}

export default appReducer;
