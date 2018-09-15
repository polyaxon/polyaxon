import { LastFetchedIds } from './utils';

export class CodeReferenceModel {
  public id: number;
  public branch: string;
  public head: string;
  public commit: string;
  public is_dirty: boolean;
  public git_url: string;
  public repo: number;
}

export class CodeReferenceStateSchema {
  public byIds: { [id: number]: CodeReferenceModel };
  public ids: number[];
  public lastFetched: LastFetchedIds;
}

export const CodeReferenceEmptyState = {
  byIds: {},
  ids: [],
  lastFetched: new LastFetchedIds()
};
