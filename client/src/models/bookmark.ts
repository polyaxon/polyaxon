import { BuildModel } from './build';
import { ExperimentModel } from './experiment';
import { GroupModel } from './group';
import { JobModel } from './job';
import { ProjectModel } from './project';

export class BookmarkModel {
  public content_object: ProjectModel | GroupModel | ExperimentModel | JobModel | BuildModel;
}
