import { LastFetchedNames } from './utils';

export class ProjectModel {
  public uuid: string;
  public name: string;
  public user: string;
  public num_experiments: number;
  public num_experiment_groups: number;
  public num_independent_experiments: number;
  public num_jobs: number;
  public num_builds: number;
  public unique_name: string;
  public is_public: boolean;
  public deleted?: boolean;
  public description?: string;
  public created_at: string;
  public updated_at: string;
  public has_tensorboard: boolean;
  public has_notebook: boolean;
  public tags: string[] = [];
  public groups: string[] = [];
  public experiments: string[] = [];
  public jobs: string[] = [];
  public builds: string[] = [];
  public bookmarked: boolean;
}

export class ProjectStateSchema {
  public byUniqueNames: {[uniqueName: string]: ProjectModel};
  public uniqueNames: string[];
  public lastFetched: LastFetchedNames;

}

export const ProjectsEmptyState = {
  byUniqueNames: {},
  uniqueNames: [],
  lastFetched: new LastFetchedNames()
};
