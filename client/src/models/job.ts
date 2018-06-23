import { LastFetched } from './utils';

export class JobModel {
  public id: number;
  public uuid: string;
  public unique_name: string;
  public name: string;
  public last_status: string;
  public user: string;
  public definition: string;
  public description: string;
  public deleted?: boolean;
  public project: string;
  public tags: Array<string> = [];
  public build_job: string;
  public created_at: string;
  public updated_at: string;
  public started_at: string;
  public finished_at: string;
  public resources: {[key: string]: any};
}

export class JobStateSchema {
  byUniqueNames: {[uniqueName: string]: JobModel};
  uniqueNames: string[];
  lastFetched: LastFetched;
}

export const JobsEmptyState = {
  byUniqueNames: {},
  uniqueNames: [],
  lastFetched: new LastFetched()
};
