import { FetchOptionAction } from './fetch';
import { PostOptionAction } from './post';

export * from './actionTypes';
export * from './fetch';
export * from './post';

export type OptionAction =
  FetchOptionAction
  | PostOptionAction;
