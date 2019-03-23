import { ArchiveJobAction } from './archive';
import { BookmarkJobAction } from './bookmark';
import { CreateJobAction } from './create';
import { DeleteJobAction } from './delete';
import { FetchJobAction } from './fetch';
import { GetJobAction } from './get';
import { RestoreJobAction } from './restore';
import { StopJobAction } from './stop';
import { UpdateJobAction } from './update';

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

export type JobAction =
  ArchiveJobAction
  | BookmarkJobAction
  | CreateJobAction
  | DeleteJobAction
  | FetchJobAction
  | GetJobAction
  | RestoreJobAction
  | StopJobAction
  | UpdateJobAction;
