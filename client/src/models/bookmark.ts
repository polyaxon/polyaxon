import { ProjectModel } from './project';
import { GroupModel } from './group';
import { ExperimentModel } from './experiment';
import { JobModel } from './job';
import { BuildModel } from './build';

export class BookmarkModel {
  public content_object: ProjectModel | GroupModel | ExperimentModel | JobModel | BuildModel;
}
