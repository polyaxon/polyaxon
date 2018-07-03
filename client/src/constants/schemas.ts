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

export const StatusSchema = new schema.Entity(
  'statuses',
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
