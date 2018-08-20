import { LastFetchedNames } from './utils';

export class ExperimentModel {
  public uuid: string;
  public unique_name: string;
  public id: number;
  public description: string;
  public user: string;
  public config: {[key: string]: any};
  public num_jobs: number;
  public last_status: string;
  public deleted?: boolean;
  public project: string;
  public experiment_group: string;
  public build_job: string;
  public has_tensorboard: boolean;
  public created_at: string;
  public updated_at: string;
  public started_at: string;
  public finished_at: string;
  public declarations: {[key: string]: any};
  public tags: string[] = [];
  public last_metric: {[metric: string]: number};
  public resources: {[key: string]: any};
  public jobs: string[] = [];
  public bookmarked: boolean;
}

export class ExperimentStateSchema {
  public byUniqueNames: {[uniqueName: string]: ExperimentModel};
  public uniqueNames: string[];
  public lastFetched: LastFetchedNames;
}

export const ExperimentsEmptyState = {
  byUniqueNames: {},
  uniqueNames: [],
  lastFetched: new LastFetchedNames()
};
