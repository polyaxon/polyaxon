import { ActivityLogsEmptyState, ActivityLogsStateSchema } from '../models/activitylog';
import { BuildsEmptyState, BuildStateSchema } from '../models/build';
import { ChartViewEmptyState, ChartViewStateSchema } from '../models/chartView';
import { CodeReferenceEmptyState, CodeReferenceStateSchema } from '../models/codeReference';
import { ErrorEmptyState, ErrorSchema } from '../models/errors';
import {
  ExperimentParamStateSchema,
  ExperimentsEmptyState,
  ExperimentsParamsEmptyState,
  ExperimentStateSchema
} from '../models/experiment';
import { ExperimentJobsEmptyState, ExperimentJobStateSchema } from '../models/experimentJob';
import { GroupsEmptyState, GroupStateSchema } from '../models/group';
import { HealthStatusEmptyState, HealthStatusStateSchema } from '../models/healthStatus';
import { JobsEmptyState, JobStateSchema } from '../models/job';
import { LoadingIndicatorEmptyState, LoadingIndicatorSchema } from '../models/loadingIndicator';
import { MetricEmptyState, MetricStateSchema } from '../models/metric';
import { ModalStateSchema } from '../models/modal';
import { NotebooksEmptyState, NotebookStateSchema } from '../models/notebook';
import { OutputsModel } from '../models/outputs';
import { ProjectsEmptyState, ProjectStateSchema } from '../models/project';
import { SearchesEmptyState, SearchesStateSchema, } from '../models/search';
import { StatusEmptyState, StatusStateSchema } from '../models/status';
import { TensorboardsEmptyState, TensorboardStateSchema } from '../models/tensorboard';
import { TokenEmptyState, TokenStateSchema } from '../models/token';
import { UserEmptyState, UserStateSchema } from '../models/user';

export interface AppState {
  projects: ProjectStateSchema;
  experiments: ExperimentStateSchema;
  experimentsParams: ExperimentParamStateSchema;
  groups: GroupStateSchema;
  jobs: JobStateSchema;
  builds: BuildStateSchema;
  tensorboards: TensorboardStateSchema;
  notebooks: NotebookStateSchema;
  experimentJobs: ExperimentJobStateSchema;
  modal: ModalStateSchema;
  auth: TokenStateSchema;
  healthStatus: HealthStatusStateSchema;
  users: UserStateSchema;
  // form: FormReducer;
  logs: string;
  outputs: OutputsModel;
  statuses: StatusStateSchema;
  metrics: MetricStateSchema;
  activityLogs: ActivityLogsStateSchema;
  searches: SearchesStateSchema;
  chartViews: ChartViewStateSchema;
  codeReferences: CodeReferenceStateSchema;
  loadingIndicators: LoadingIndicatorSchema;
  errors: ErrorSchema;
}

export const AppEmptyState = {
  projects: ProjectsEmptyState,
  experiments: ExperimentsEmptyState,
  experimentsParams: ExperimentsParamsEmptyState,
  groups: GroupsEmptyState,
  jobs: JobsEmptyState,
  builds: BuildsEmptyState,
  tensorboards: TensorboardsEmptyState,
  notebooks: NotebooksEmptyState,
  experimentJobs: ExperimentJobsEmptyState,
  auth: TokenEmptyState,
  healthStatus: HealthStatusEmptyState,
  user: UserEmptyState,
  logs: '',
  statuses: StatusEmptyState,
  metrics: MetricEmptyState,
  activityLogs: ActivityLogsEmptyState,
  searches: SearchesEmptyState,
  chartViews: ChartViewEmptyState,
  codeReferences: CodeReferenceEmptyState,
  loadingIndicators: LoadingIndicatorEmptyState,
  errors: ErrorEmptyState,
};
