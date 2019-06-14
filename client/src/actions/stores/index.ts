import { CreateStoreAction } from './create';
import { DeleteStoreAction } from './delete';
import { FetchStoreAction } from './fetch';
import { GetStoreAction } from './get';
import { InitStoreAction } from './init';
import { UpdateStoreAction } from './update';

export * from './actionTypes';
export * from './create';
export * from './delete';
export * from './fetch';
export * from './get';
export * from './update';
export * from './init';

export type StoreAction =
  | CreateStoreAction
  | DeleteStoreAction
  | FetchStoreAction
  | GetStoreAction
  | UpdateStoreAction
  | InitStoreAction;
