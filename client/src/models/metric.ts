import { LastFetchedIds } from './utils';

export class MetricModel {
  public id: number;
  public created_at: string;
  public values: { [key: string]: any };
}

export class MetricStateSchema {
  public byIds: { [id: number]: MetricModel };
  public ids: number[];
  public lastFetched: LastFetchedIds;
}

export const MetricEmptyState = {
  byIds: {},
  ids: [],
  lastFetched: new LastFetchedIds()
};
