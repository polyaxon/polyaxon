import { BaseEmptyState, BaseState, RunFieldSchema } from '../../forms';

export interface State extends BaseState {
  config: string;
  run: RunFieldSchema;
}

export const EmptyState = {...BaseEmptyState, config: '', run: {}};
