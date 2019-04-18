import { LastFetchedNames } from './utils';

export class TensorboardModel {
  public id: number;
  public uuid: string;
  public unique_name: string;
  public pod_id: string;
  public name: string;
  public user: string;
  public definition: string;
  public description: string;
  public is_managed: boolean;
  public backend: string;
  public deleted?: boolean;
  public project: string;
  public build_job: string;
  public group: string;
  public experiment: string;
  public experiment_group: string;
  public tags: string[] = [];
  public last_status: string;
  public created_at: string;
  public updated_at: string;
  public started_at: string;
  public finished_at: string;
  public config: { [key: string]: any };
  public resources: { [key: string]: any };
  public node_scheduled: string;
  public bookmarked: boolean;
}

export class TensorboardStateSchema {
  public byUniqueNames: { [uniqueName: string]: TensorboardModel };
  public uniqueNames: string[];
  public lastFetched: LastFetchedNames;
}

export const TensorboardsEmptyState = {
  byUniqueNames: {},
  uniqueNames: [],
  lastFetched: new LastFetchedNames()
};
