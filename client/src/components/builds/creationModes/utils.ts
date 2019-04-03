import { BaseEmptyState, BaseState, BuildFieldSchema } from '../../forms';

export interface State extends BaseState {
  config: string;
  build: BuildFieldSchema;
}

export const EmptyState = {...BaseEmptyState, config: '', build: {}};
