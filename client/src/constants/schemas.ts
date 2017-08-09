import { schema } from 'normalizr';

export const ExperimentSchema = new schema.Entity('experiments');

export const ProjectSchema = new schema.Entity('projects', {
  experiments: [ExperimentSchema]
});
