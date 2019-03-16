import { BuildModel } from './build';
import { ExperimentModel } from './experiment';
import { GroupModel } from './group';
import { JobModel } from './job';
import { NotebookModel } from './notebook';
import { ProjectModel } from './project';
import { TensorboardModel } from './tensorboard';

export class BookmarkModel {
  public content_object: ProjectModel
    | GroupModel
    | ExperimentModel
    | JobModel
    | BuildModel
    | TensorboardModel
    | NotebookModel;
}
