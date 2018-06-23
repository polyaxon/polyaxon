// import { FormReducer } from 'redux-form';

import { ProjectStateSchema, ProjectsEmptyState } from '../models/project';
import { ExperimentStateSchema, ExperimentsEmptyState } from '../models/experiment';
import { ExperimentJobStateSchema, ExperimentJobsEmptyState } from '../models/experimentJob';
import { JobStateSchema, JobsEmptyState } from '../models/job';
import { GroupStateSchema, GroupsEmptyState } from '../models/group';
import { TokenStateSchema, TokenEmptyState } from '../models/token';
import { ModalStateSchema } from '../models/modal';
import { UserEmptyState, UserStateSchema } from '../models/user';
import { BuildsEmptyState, BuildStateSchema } from '../models/build';

export interface AppState {
  projects: ProjectStateSchema;
  experiments: ExperimentStateSchema;
  groups: GroupStateSchema;
  jobs: JobStateSchema;
  builds: BuildStateSchema;
  experimentJobs: ExperimentJobStateSchema;
  modal: ModalStateSchema;
  auth: TokenStateSchema;
  users: UserStateSchema;
  // form: FormReducer;
  logs: string;
}

export const AppEmptyState = {
  projects: ProjectsEmptyState,
  experiments: ExperimentsEmptyState,
  groups: GroupsEmptyState,
  jobs: JobsEmptyState,
  builds: BuildsEmptyState,
  experimentJobs: ExperimentJobsEmptyState,
  auth: TokenEmptyState,
  user: UserEmptyState
};
