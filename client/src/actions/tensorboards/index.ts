import { ArchiveTensorboardAction } from './archive';
import { BookmarkTensorboardAction } from './bookmark';
import { DeleteTensorboardAction } from './delete';
import { FetchTensorboardAction } from './fetch';
import { GetTensorboardAction } from './get';
import { RestoreTensorboardAction } from './restore';
import { StopTensorboardAction } from './stop';
import { UpdateTensorboardAction } from './update';

export * from './actionTypes';
export * from './archive';
export * from './bookmark';
export * from './delete';
export * from './fetch';
export * from './get';
export * from './restore';
export * from './stop';
export * from './update';

export type TensorboardAction =
  ArchiveTensorboardAction
  | BookmarkTensorboardAction
  | DeleteTensorboardAction
  | FetchTensorboardAction
  | GetTensorboardAction
  | RestoreTensorboardAction
  | StopTensorboardAction
  | UpdateTensorboardAction;
