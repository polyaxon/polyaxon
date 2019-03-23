import { ArchiveGroupAction } from './archive';
import { BookmarkGroupAction } from './bookmark';
import { CreateGroupAction } from './create';
import { DeleteGroupAction } from './delete';
import { FetchGroupAction } from './fetch';
import { GetGroupAction } from './get';
import { RestoreGroupAction } from './restore';
import { StopGroupAction } from './stop';
import { TensorboardGroupAction } from './tensorboard';
import { UpdateGroupAction } from './update';

export * from './actionTypes';
export * from './archive';
export * from './bookmark';
export * from './create';
export * from './delete';
export * from './fetch';
export * from './get';
export * from './restore';
export * from './stop';
export * from './tensorboard';
export * from './update';

export type GroupAction =
  ArchiveGroupAction
  | BookmarkGroupAction
  | CreateGroupAction
  | DeleteGroupAction
  | FetchGroupAction
  | GetGroupAction
  | RestoreGroupAction
  | StopGroupAction
  | TensorboardGroupAction
  | UpdateGroupAction;
