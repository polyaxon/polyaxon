import { LastFetchedNames } from './utils';

export class StoreModel {
  public id: string;
  public uuid: string;
  public name: string;
  public readme: string;
  public description: string;
  public tags: string[] = [];
  public deleted?: boolean;
  public created_at: string;
  public updated_at: string;
  public type: string;
  public mount_path: string;
  public host_path: string;
  public volume_claim: string;
  public bucket: string;
  public k8s_secret: string;
  public read_only: boolean;
}

export class StoreStateSchema {
  public byUniqueNames: { [uniqueName: string]: StoreModel };
  public uniqueNames: string[];
  public lastFetched: LastFetchedNames;
}

export const StoresEmptyState = {
  byUniqueNames: {},
  uniqueNames: [],
  lastFetched: new LastFetchedNames()
};
