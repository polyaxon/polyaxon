import { LastFetchedNames } from './utils';

export class AccessModel {
  public id: string;
  public uuid: string;
  public name: string;
  public readme: string;
  public description: string;
  public tags: string[] = [];
  public deleted?: boolean;
  public created_at: string;
  public updated_at: string;
  public host: string;
  public k8s_secret: string;
  public is_default: boolean;
}

export class AccessStateSchema {
  public byUniqueNames: { [uniqueName: string]: AccessModel };
  public uniqueNames: string[];
  public lastFetched: LastFetchedNames;
}

export const AccessesEmptyState = {
  byUniqueNames: {},
  uniqueNames: [],
  lastFetched: new LastFetchedNames()
};
