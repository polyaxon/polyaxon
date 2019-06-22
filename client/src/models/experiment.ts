import { LastFetchedNames } from './utils';

export class ExperimentModel {
  public uuid: string;
  public unique_name: string;
  public name: string;
  public id: number;
  public original: string;
  public cloning_strategy: string;
  public description: string;
  public is_managed: boolean;
  public backend: string;
  public framework: string;
  public user: string;
  public content: string;
  public num_jobs: number;
  public last_status: string;
  public deleted?: boolean;
  public project: string;
  public experiment_group: string;
  public build_job: string;
  public code_reference: number;
  public has_tensorboard: boolean;
  public created_at: string;
  public updated_at: string;
  public started_at: string;
  public finished_at: string;
  public params: { [key: string]: any };
  public tags: string[] = [];
  public last_metric: { [metric: string]: number };
  public data_refs: { [key: string]: string };
  public resources: { [key: string]: any };
  public run_env: { [key: string]: any };
  public jobs: string[] = [];
  public readme: string;
  public bookmarked: boolean;
}

export class ExperimentStateSchema {
  public byUniqueNames: { [uniqueName: string]: ExperimentModel };
  public uniqueNames: string[];
  public lastFetched: LastFetchedNames;
}

export const ExperimentsEmptyState = {
  byUniqueNames: {},
  uniqueNames: [],
  lastFetched: new LastFetchedNames()
};

export class ExperimentParamStateSchema {
  public byUniqueNames: { [uniqueName: string]: ExperimentModel };
  public uniqueNames: string[];
  public lastFetched: LastFetchedNames;
}

export const ExperimentsParamsEmptyState = {
  byUniqueNames: {},
  uniqueNames: [],
  lastFetched: new LastFetchedNames()
};
