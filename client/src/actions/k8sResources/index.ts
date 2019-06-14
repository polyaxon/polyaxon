import { CreateK8SResourceAction } from './create';
import { DeleteK8SResourceAction } from './delete';
import { FetchK8SResourceAction } from './fetch';
import { FetchK8SResourceNameAction } from './fetch_names';
import { GetK8SResourceAction } from './get';
import { InitK8SResourceAction } from './init';
import { UpdateK8SResourceAction } from './update';

export * from './actionTypes';
export * from './create';
export * from './delete';
export * from './fetch';
export * from './fetch_names';
export * from './get';
export * from './update';
export * from './init';

export type K8SResourceAction =
  | CreateK8SResourceAction
  | DeleteK8SResourceAction
  | FetchK8SResourceAction
  | FetchK8SResourceNameAction
  | GetK8SResourceAction
  | UpdateK8SResourceAction
  | InitK8SResourceAction;
