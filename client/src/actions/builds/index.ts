import { ArchiveBuildAction } from './archive';
import { BookmarkBuildAction } from './bookmark';
import { CreateBuildAction } from './create';
import { DeleteBuildAction } from './delete';
import { FetchBuildAction } from './fetch';
import { GetBuildAction } from './get';
import { RestoreBuildAction } from './restore';
import { StopBuildAction } from './stop';
import { UpdateBuildAction } from './update';

export * from './actionTypes';
export * from './archive';
export * from './bookmark';
export * from './create';
export * from './delete';
export * from './fetch';
export * from './get';
export * from './restore';
export * from './stop';
export * from './update';

export type BuildAction =
  ArchiveBuildAction
  | BookmarkBuildAction
  | CreateBuildAction
  | DeleteBuildAction
  | FetchBuildAction
  | GetBuildAction
  | RestoreBuildAction
  | StopBuildAction
  | UpdateBuildAction;
