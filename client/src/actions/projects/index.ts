import { ArchiveProjectAction } from './archive';
import { BookmarkProjectAction } from './bookmark';
import { CreateProjectAction } from './create';
import { DeleteProjectAction } from './delete';
import { FetchProjectAction } from './fetch';
import { GetProjectAction } from './get';
import { NotebookProjectAction } from './notebook';
import { RestoreProjectAction } from './restore';
import { TensorboardProjectAction } from './tensorboard';
import { UpdateProjectAction } from './update';

export * from './actionTypes';
export * from './archive';
export * from './bookmark';
export * from './create';
export * from './delete';
export * from './fetch';
export * from './get';
export * from './notebook';
export * from './restore';
export * from './tensorboard';
export * from './update';

export type ProjectAction =
  ArchiveProjectAction
  | BookmarkProjectAction
  | CreateProjectAction
  | DeleteProjectAction
  | FetchProjectAction
  | GetProjectAction
  | NotebookProjectAction
  | RestoreProjectAction
  | TensorboardProjectAction
  | UpdateProjectAction;
