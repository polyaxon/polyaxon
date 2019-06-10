import { LastFetchedNames } from './utils';

export class OptionModel {
  public key: string;
  public typing: string;
  public is_secret: boolean;
  public value: any;
  public description: string;
}

export class OptionStateSchema {
  public byUniqueNames: { [uniqueName: string]: OptionModel };
  public uniqueNames: string[];
  public lastFetched: LastFetchedNames;
}

export const OptionsEmptyState = {
  byUniqueNames: {},
  uniqueNames: [],
  lastFetched: new LastFetchedNames()
};
