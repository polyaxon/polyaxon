import { connect } from 'react-redux';

import * as actions from '../actions/search';
import FilterList from '../components/filters/filterList';
import { AppState } from '../constants/types';
import { FilterOption } from '../interfaces/filterOptions';
import { SearchModel } from '../models/search';

export interface Params {
  query?: string;
  sort?: string;
  handleFilter: (query: string, sort: string) => any;
  sortOptions: string[];
  filterOptions: FilterOption[];
  defaultSort?: string;
  fetchSearches?: () => actions.SearchAction;
}

export function mapStateToProps(state: AppState, params: Params) {
  const searchIds = state.searches.lastFetched.ids;
  const count = state.searches.lastFetched.count;
  const searches: SearchModel[] = [];
  searchIds.forEach(
    (searchId: number) => {
      searches.push(state.searches.byIds[searchId]);
    });
  return {
    query: params.query,
    sort: params.sort,
    handleFilter: params.handleFilter,
    sortOptions: params.sortOptions,
    filterOptions: params.filterOptions,
    defaultSort: params.defaultSort,
    fetchSearches: params.fetchSearches,
    searches,
    searchesCount: count,
  };
}

export default connect(mapStateToProps, {})(FilterList);
