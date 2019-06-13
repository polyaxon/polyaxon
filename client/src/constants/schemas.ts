import { schema } from 'normalizr';

export const JobSchema = new schema.Entity(
  'jobs',
  {},
  {
    idAttribute: 'unique_name'
  });

export const BuildSchema = new schema.Entity(
  'builds',
  {},
  {
    idAttribute: 'unique_name'
  });

export const NotebookSchema = new schema.Entity(
  'notebooks',
  {},
  {
    idAttribute: 'unique_name'
  });

export const TensorboardSchema = new schema.Entity(
  'tensorboards',
  {},
  {
    idAttribute: 'unique_name'
  });

export const StatusSchema = new schema.Entity(
  'statuses',
  {},
  {
    idAttribute: 'id'
  });

export const MetricSchema = new schema.Entity(
  'metrics',
  {},
  {
    idAttribute: 'id'
  });

export const ExperimentJobSchema = new schema.Entity(
  'experimentJobs',
  {},
  {
    idAttribute: 'unique_name'
  });

export const GroupSchema = new schema.Entity(
  'groups',
  {},
  {
    idAttribute: 'unique_name'
  });

export const ExperimentSchema = new schema.Entity(
  'experiments',
  {},
  {
    idAttribute: 'unique_name'
  });

export const ProjectSchema = new schema.Entity(
  'projects',
  {experiments: [ExperimentSchema]},
  {
    idAttribute: 'unique_name'
  });

export const UserSchema = new schema.Entity(
  'users',
  {},
  {
    idAttribute: 'username'
  });

export const activityLogSchema = new schema.Entity(
  'activityLogs',
  {},
  {
    idAttribute: 'id'
  });

export const searchSchema = new schema.Entity(
  'searches',
  {},
  {
    idAttribute: 'id'
  });

export const chartViewSchema = new schema.Entity(
  'chartViews',
  {},
  {
    idAttribute: 'id'
  });

export const codeReferenceSchema = new schema.Entity(
  'codeReferences',
  {},
  {
    idAttribute: 'id'
  });

export const OptionSchema = new schema.Entity(
  'options',
  {},
  {
    idAttribute: 'key'
  });

export const K8SResourceSchema = new schema.Entity(
  'k8sResources',
  {},
  {
    idAttribute: 'name'
  });
