import { LastFetchedIds } from './utils';

export class MetricModel {
  public id: number;
  public created_at: string;
  public values: {[key: string]: any};
}

export class MetricStateSchema {
  byIds: {[id: number]: MetricModel};
  ids: number[];
  lastFetched: LastFetchedIds;
}

export const MetricEmptyState = {
  byIds: {},
  ids: [],
  lastFetched: new LastFetchedIds()
};
