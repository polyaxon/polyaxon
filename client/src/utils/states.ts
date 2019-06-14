import { getPaginatedSlice } from '../constants/paginate';
import { AppState } from '../constants/types';
import { getExperimentIndexName } from '../constants/utils';
import { BuildModel, BuildStateSchema } from '../models/build';
import { ExperimentModel, ExperimentStateSchema } from '../models/experiment';
import { ExperimentJobModel, ExperimentJobStateSchema } from '../models/experimentJob';
import { GroupModel, GroupStateSchema } from '../models/group';
import { JobModel, JobStateSchema } from '../models/job';
import { K8SResourceModel, K8SResourceStateSchema } from '../models/k8sResource';
import { NotebookModel, NotebookStateSchema } from '../models/notebook';
import { ProjectModel, ProjectStateSchema } from '../models/project';
import { StoreModel, StoreStateSchema } from '../models/store';
import { TensorboardModel, TensorboardStateSchema } from '../models/tensorboard';
import { getGroupName } from '../urls/utils';

export const getLastFetchedProjects = (projectsState: ProjectStateSchema) => {
  const projectNames = projectsState.lastFetched.names;
  const count = projectsState.lastFetched.count;
  const projects: ProjectModel[] = [];
  projectNames.forEach(
    (project: string, idx: number) => {
      projects.push(projectsState.byUniqueNames[project]);
    });
  return {projects, count};
};

export const getFilteredProjects = (state: AppState, username: string) => {
  const projects: ProjectModel[] = [];
  const user = state.users.byUserNames[username];
  if (user == null) {
    return {user: username, projects: [] as ProjectModel[], count: 0};
  }
  let projectNames = user.projects;
  projectNames = getPaginatedSlice(projectNames);
  projectNames.forEach(
    (project: string, idx: number) => {
      projects.push(state.projects.byUniqueNames[project]);
    });
  return {projects, count: user.num_projects};
};

export const getLastFetchedBuilds = (buildsState: BuildStateSchema) => {
  const buildNames = buildsState.lastFetched.names;
  const count = buildsState.lastFetched.count;
  const builds: BuildModel[] = [];
  buildNames.forEach(
    (build: string, idx: number) => {
      builds.push(buildsState.byUniqueNames[build]);
    });
  return {builds, count};
};

export const getFilteredBuilds = (state: AppState, projectName: string) => {
  const builds: BuildModel[] = [];
  const project = state.projects.byUniqueNames[projectName];
  const BuildNames = project.builds;
  BuildNames.forEach(
    (build: string, idx: number) => {
      builds.push(state.builds.byUniqueNames[build]);
    });
  return {builds, count: project.num_builds};
};

export const getLastFetchedExperimentJobs = (experimentJobsState: ExperimentJobStateSchema) => {
  const jobNames = experimentJobsState.lastFetched.names;
  const count = experimentJobsState.lastFetched.count;
  const jobs: ExperimentJobModel[] = [];
  jobNames.forEach(
    (job: string, idx: number) => {
      jobs.push(experimentJobsState.byUniqueNames[job]);
    });
  return {jobs, count};
};

export const getFilteredExperimentJobs = (state: AppState, experimentUniqueName: string) => {
  const experimentName = getExperimentIndexName(experimentUniqueName);
  const jobs: ExperimentJobModel[] = [];
  const experiment = state.experiments.byUniqueNames[experimentName];
  const jobNames = experiment.jobs;
  jobNames.forEach(
    (job: string, idx: number) => {
      jobs.push(state.experimentJobs.byUniqueNames[job]);
    });
  return {jobs, count: experiment.num_jobs};
};

export const getLastFetchedExperiments = (experimentsState: ExperimentStateSchema) => {
  const experimentNames = experimentsState.lastFetched.names;
  const count = experimentsState.lastFetched.count;
  const experiments: ExperimentModel[] = [];
  experimentNames.forEach(
    (experiment: string, idx: number) => {
      experiments.push(experimentsState.byUniqueNames[getExperimentIndexName(experiment)]);
    });
  return {experiments, count};
};

export const getFilteredExperiments = (state: AppState, projectName: string, groupId?: number | string) => {
  const groupName = groupId != null ? getGroupName(projectName, groupId) : null;
  const experiments: ExperimentModel[] = [];
  let count = 0;
  if (groupName != null) {
    const group = state.groups.byUniqueNames[groupName];
    count = group.num_experiments;
    let experimentNames = group.experiments;
    experimentNames = getPaginatedSlice(experimentNames);
    experimentNames.forEach(
      (experiment: string, idx: number) => {
        experiments.push(state.experiments.byUniqueNames[experiment]);
      });
  } else {
    const project = state.projects.byUniqueNames[projectName];
    count = project.num_independent_experiments;
    let experimentNames = project.experiments.filter(
      (experiment) => state.experiments.byUniqueNames[experiment].experiment_group == null
    );
    experimentNames = getPaginatedSlice(experimentNames);
    experimentNames.forEach(
      function(experiment: string, idx: number) {
        experiments.push(state.experiments.byUniqueNames[experiment]);
      });
  }
  return {experiments, count};
};

export const getLastFetchedGroups = (groupsState: GroupStateSchema) => {
  const groupNames = groupsState.lastFetched.names;
  const count = groupsState.lastFetched.count;
  const groups: GroupModel[] = [];
  groupNames.forEach(
    (group: string, idx: number) => {
      groups.push(groupsState.byUniqueNames[group]);
    });
  return {groups, count};
};

export const getFilteredGroups = (state: AppState, projectName: string) => {
  const groups: GroupModel[] = [];
  const project = state.projects.byUniqueNames[projectName];
  let groupNames = project.groups;
  groupNames = getPaginatedSlice(groupNames);
  groupNames.forEach(
    (group: string, idx: number) => {
      groups.push(state.groups.byUniqueNames[group]);
    });
  return {groups, count: project.num_experiment_groups};
};

export const getLastFetchedJobs = (jobsState: JobStateSchema) => {
  const jobNames = jobsState.lastFetched.names;
  const count = jobsState.lastFetched.count;
  const jobs: JobModel[] = [];
  jobNames.forEach(
    (job: string, idx: number) => {
      jobs.push(jobsState.byUniqueNames[job]);
    });
  return {jobs, count};
};

export const getFilteredJobs = (state: AppState, projectName: string) => {
  const jobs: JobModel[] = [];
  const project = state.projects.byUniqueNames[projectName];
  let jobNames = project.jobs;
  jobNames = getPaginatedSlice(jobNames);
  jobNames.forEach(
    (job: string, idx: number) => {
      jobs.push(state.jobs.byUniqueNames[job]);
    });
  return {jobs, count: project.num_jobs};
};

const getLastFetched = (entitySchema: any, entities: any[]) => {
  const entityNames = entitySchema.lastFetched.names;
  const count = entitySchema.lastFetched.count;
  entityNames.forEach(
    (build: string, idx: number) => {
      entities.push(entitySchema.byUniqueNames[build]);
    });
  return {entities, count};
};

export const getLastFetchedNotebooks = (notebooksState: NotebookStateSchema) => {
  const notebookNames = notebooksState.lastFetched.names;
  const count = notebooksState.lastFetched.count;
  const notebooks: NotebookModel[] = [];
  notebookNames.forEach(
    (build: string, idx: number) => {
      notebooks.push(notebooksState.byUniqueNames[build]);
    });
  return {notebooks, count};
};

export const getLastFetchedTensorboards = (tensorboardsState: TensorboardStateSchema) => {
  const tensorboardNames = tensorboardsState.lastFetched.names;
  const count = tensorboardsState.lastFetched.count;
  const tensorboards: TensorboardModel[] = [];
  tensorboardNames.forEach(
    (tensorboard: string, idx: number) => {
      tensorboards.push(tensorboardsState.byUniqueNames[tensorboard]);
    });
  return {tensorboards, count};
};

export const getLastFetchedK8SResources = (k8sResourcesState: K8SResourceStateSchema) => {
  const k8sResourcesNames = k8sResourcesState.lastFetched.names;
  const count = k8sResourcesState.lastFetched.count;
  const k8sResources: K8SResourceModel[] = [];
  k8sResourcesNames.forEach(
    (resource: string, idx: number) => {
      k8sResources.push(k8sResourcesState.byUniqueNames[resource]);
    });
  return {k8sResources, count};
};

export const getLastFetchedStores = (storesState: StoreStateSchema) => {
  const storesNames = storesState.lastFetched.names;
  const count = storesState.lastFetched.count;
  const stores: StoreModel[] = [];
  storesNames.forEach(
    (resource: string, idx: number) => {
      stores.push(storesState.byUniqueNames[resource]);
    });
  return {stores, count};
};
