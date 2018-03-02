export class ProjectModel {
  public uuid: string;
  public name: string;
  public user: string;
  public num_experiments: number;
  public num_experiment_groups: number;
  public num_independent_experiments: number;
  public unique_name: string;
  public is_public: boolean;
  public deleted?: boolean;
  public description?: string;
  public created_at: string;
  public updated_at: string;
  public has_tensorboard: boolean;
  public has_notebook: boolean;
  public groups: Array<string> = [];
  public experiments: Array<string> = [];
}

export class ProjectStateSchema {
  byUniqueNames: {[uniqueName: string]: ProjectModel};
  uniqueNames: string[];
}

export const ProjectsEmptyState = {byUniqueNames: {}, uniqueNames: []};
