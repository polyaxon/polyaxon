import { ChartModel } from './chart';
import { LastFetchedIds } from './utils';

export class ChartViewModel {
  public id: number;
  public created_at: string;
  public charts: ChartModel[];
  public name: string;
}

export class ChartViewStateSchema {
  public byIds: { [id: number]: ChartViewModel };
  public ids: number[];
  public lastFetched: LastFetchedIds;
}

export const ChartViewEmptyState = {
  byIds: {},
  ids: [],
  lastFetched: new LastFetchedIds()
};
