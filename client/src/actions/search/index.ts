import { CreateSearchAction } from './create';
import { DeleteSearchAction } from './delete';
import { FetchSearchAction } from './fetch';
import { GetSearchAction } from './get';

export * from './actionTypes';
export * from './create';
export * from './delete';
export * from './fetch';
export * from './get';

export type SearchAction =
  | CreateSearchAction
  | DeleteSearchAction
  | FetchSearchAction
  | GetSearchAction;
