import { LastFetchedNames } from './utils';

export class JobModel {
  public id: number;
  public uuid: string;
  public unique_name: string;
  public pod_id: string;
  public name: string;
  public original: string;
  public cloning_strategy: string;
  public last_status: string;
  public is_managed: boolean;
  public backend: string;
  public user: string;
  public definition: string;
  public description: string;
  public readme: string;
  public deleted?: boolean;
  public project: string;
  public tags: string[] = [];
  public build_job: string;
  public created_at: string;
  public updated_at: string;
  public started_at: string;
  public finished_at: string;
  public resources: { [key: string]: any };
  public config: { [key: string]: any };
  public node_scheduled: string;
  public bookmarked: boolean;
}

export class JobStateSchema {
  public byUniqueNames: { [uniqueName: string]: JobModel };
  public uniqueNames: string[];
  public lastFetched: LastFetchedNames;
}

export const JobsEmptyState = {
  byUniqueNames: {},
  uniqueNames: [],
  lastFetched: new LastFetchedNames()
};
