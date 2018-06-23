import { LastFetched } from './utils';

export class BuildModel {
  public id: number;
  public uuid: string;
  public unique_name: string;
  public name: string;
  public user: string;
  public definition: string;
  public description: string;
  public deleted?: boolean;
  public project: string;
  public tags: Array<string> = [];
  public last_status: string;
  public created_at: string;
  public updated_at: string;
  public started_at: string;
  public finished_at: string;
  public resources: {[key: string]: any};
}

export class BuildStateSchema {
  byUniqueNames: {[uniqueName: string]: BuildModel};
  uniqueNames: string[];
  lastFetched: LastFetched;
}

export const BuildsEmptyState = {
  byUniqueNames: {},
  uniqueNames: [],
  lastFetched: new LastFetched()
};
