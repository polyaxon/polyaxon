import { connect } from 'react-redux';

import * as actions from '../../actions/search';
import * as search_actions from '../../actions/search';
import FilterList from '../../components/filters/filterList';
import { AppState } from '../../constants/types';
import { ColumnInterface } from '../../interfaces/tableColumns';
import { SearchModel } from '../../models/search';

export interface Props {
  query?: string;
  sort?: string;
  handleFilter: (query: string, sort: string) => any;
  sortOptions: string[];
  columnOptions: ColumnInterface[];
  defaultSort?: string;
  fetchSearches?: () => actions.SearchAction;
  createSearch?: (data: SearchModel) => search_actions.SearchAction;
  deleteSearch?: (searchId: number) => search_actions.SearchAction;
  selectSearch?: (data: SearchModel) => void;
}

export function mapStateToProps(state: AppState, props: Props) {
  const searchIds = state.searches.lastFetched.ids;
  const count = state.searches.lastFetched.count;
  const searches: SearchModel[] = [];
  searchIds.forEach(
    (searchId: number) => {
      searches.push(state.searches.byIds[searchId]);
    });
  return {
    query: props.query,
    sort: props.sort,
    handleFilter: props.handleFilter,
    sortOptions: props.sortOptions,
    columnOptions: props.columnOptions,
    defaultSort: props.defaultSort,
    fetchSearches: props.fetchSearches,
    createSearch: props.createSearch,
    deleteSearch: props.deleteSearch,
    searches,
    searchesCount: count,
  };
}

export default connect(mapStateToProps, {})(FilterList);
