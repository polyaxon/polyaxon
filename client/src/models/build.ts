export class BuildModel {
  public uuid: string;
  public unique_name: string;
  public name: string;
  public id: number;
  public last_status: string;
  public definition: string;
  public deleted?: boolean;
  public project: string;
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
}

export const BuildsEmptyState = {byUniqueNames: {}, uniqueNames: []};
