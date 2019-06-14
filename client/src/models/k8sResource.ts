import { LastFetchedNames } from './utils';

export class K8SResourceModel {
  public id: string;
  public uuid: string;
  public name: string;
  public readme: string;
  public description: string;
  public tags: string[] = [];
  public deleted?: boolean;
  public created_at: string;
  public updated_at: string;
  public items: string[];
  public k8s_ref: string;
}

export class K8SResourceStateSchema {
  public byUniqueNames: { [uniqueName: string]: K8SResourceModel };
  public uniqueNames: string[];
  public lastFetched: LastFetchedNames;
}

export const K8SResourcesEmptyState = {
  byUniqueNames: {},
  uniqueNames: [],
  lastFetched: new LastFetchedNames()
};
