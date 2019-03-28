import { SearchModel } from '../../models/search';

export const DefaultSearches = [
  {
    id: 1,
    name: 'running [default]',
    query: {query: 'status: building|scheduled|starting|running', sort: '-updated_at'}
  } as SearchModel,
  {
    id: 2,
    name: 'succeeded [default]',
    query: {query: 'status: succeeded', sort: '-finished_at'}
  } as SearchModel,
  {
    id: 3,
    name: 'failed [default]',
    query: {query: 'status: failed', sort: '-finished_at'}
  } as SearchModel
];
