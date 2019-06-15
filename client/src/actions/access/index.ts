import { CreateAccessAction } from './create';
import { DeleteAccessAction } from './delete';
import { FetchAccessAction } from './fetch';
import { GetAccessAction } from './get';
import { InitAccessAction } from './init';
import { UpdateAccessAction } from './update';

export * from './actionTypes';
export * from './create';
export * from './delete';
export * from './fetch';
export * from './get';
export * from './update';
export * from './init';

export type AccessAction =
  | CreateAccessAction
  | DeleteAccessAction
  | FetchAccessAction
  | GetAccessAction
  | UpdateAccessAction
  | InitAccessAction;
