import { LastFetchedIds } from './utils';

export class SearchModel {
  public id: number;
  public name: string;
  public query: {[key: string]: string};
}

export class SearchesStateSchema {
  public byIds: {[id: number]: SearchModel};
  public ids: number[];
  public lastFetched: LastFetchedIds;
}

export const SearchesEmptyState = {
  byIds: {},
  ids: [],
  lastFetched: new LastFetchedIds()
};
