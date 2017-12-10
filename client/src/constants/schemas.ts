import { schema } from 'normalizr';

export const ExperimentSchema = new schema.Entity('experiments', {}, { idAttribute: 'uuid' });

export const ProjectSchema = new schema.Entity('projects', {
  experiments: [ExperimentSchema]
}, { idAttribute: 'uuid' });
