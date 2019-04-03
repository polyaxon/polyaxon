import { BaseEmptyState, BaseState } from '../../forms';

export interface State extends BaseState {
  config: string;
  dockerImage: string;
}

export const EmptyState = {...BaseEmptyState, config: '', dockerImage: ''};
