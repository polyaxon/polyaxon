import { BaseEmptyState, BaseState } from '../../forms';

export interface State extends BaseState {
  config: string;
  hptuning: object;
}

export const EmptyState = {...BaseEmptyState, config: '', hptuning: {}};
