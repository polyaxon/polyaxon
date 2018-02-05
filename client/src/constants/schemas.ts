import { schema } from 'normalizr';

export const JobSchema = new schema.Entity(
  'jobs', {}, { idAttribute: 'unique_name' });

export const GroupSchema = new schema.Entity(
  'groups', {}, { idAttribute: 'unique_name' });

export const ExperimentSchema = new schema.Entity(
  'experiments', {}, { idAttribute: 'unique_name' });

export const ProjectSchema = new schema.Entity(
  'projects', {experiments: [ExperimentSchema]}, { idAttribute: 'unique_name' });
