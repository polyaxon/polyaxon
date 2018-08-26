import * as React from 'react';
import { Pager } from 'react-bootstrap';

import * as deepEqual from 'deep-equal';
import * as queryString from 'query-string';

import { PAGE_SIZE, paginate, paginateNext, paginatePrevious } from '../constants/paginate';
import { FilterOption } from '../interfaces/filterOptions';
import { DEFAULT_FILTERS } from './filters/constants';
import FilterList from './filters/filterList';
import './paginatedTable.less';

export interface Props {
  count: number;
  componentList: React.ReactNode;
  componentEmpty: React.ReactNode;
  filters: boolean | string;
  fetchData: (offset: number, query?: string, sort?: string, extraFilters?: {}) => any;
  sortOptions?: string[];
  filterOptions?: FilterOption[];
}

interface State {
  offset: number;
  query?: string;
  sort?: string;
  extraFilters?: { [key: string]: number | boolean | string };
}

export default class PaginatedTable extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = this.getFilters();
  }

  public getFilters() {
    const filters = {offset: 0, query: '', sort: '', extraFilters: {}};
    const pieces = location.href.split('?');
    if (pieces.length > 1) {
      const search = queryString.parse(pieces[1]);
      if (search.offset) {
        filters.offset = parseInt(search.offset, 10);
        delete search.offset;
      }
      if (search.query) {
        filters.query = search.query;
        delete search.query;
      }
      if (search.sort) {
        filters.sort = search.sort;
        delete search.sort;
      }
      if (Object.keys(search).length > 0) {
        filters.extraFilters = search;
      }
    }
    return filters;
  }

  public componentDidMount() {
    this.props.fetchData(
      this.state.offset,
      this.state.query,
      this.state.sort,
      this.state.extraFilters);
  }

  public componentDidUpdate(prevProps: Props, prevState: State) {
    let changed = false;
    if (this.state.offset !== prevState.offset) {
      changed = true;
    }
    if (this.state.query !== prevState.query) {
      changed = true;
      this.setState({offset: 0});
    }
    if (this.state.sort !== prevState.sort) {
      changed = true;
      this.setState({offset: 0});
    }
    if (this.state.extraFilters &&
      prevState.extraFilters &&
      !deepEqual(this.state.extraFilters, prevState.extraFilters)) {
      changed = true;
      this.setState({offset: 0});
    }
    if (changed) {
      this.props.fetchData(
        this.state.offset,
        this.state.query,
        this.state.sort,
        this.state.extraFilters);
    }
  }

  public handleNextPage = () => {
    this.setState((prevState, prevProps) => ({
      offset: prevState.offset + PAGE_SIZE,
    }));
  };

  public handlePreviousPage = () => {
    this.setState((prevState, prevProps) => ({
      offset: prevState.offset - PAGE_SIZE,
    }));
  };

  public handleFilter = (query: string, sort: string, extraFilters?: { [key: string]: number | boolean | string }) => {
    this.setState((prevState, prevProps) => ({
      query,
      sort,
      extraFilters,
    }));
  };

  public render() {
    const getFilters = () => {
      if (this.props.filters === DEFAULT_FILTERS) {
        return (
          <FilterList
            query={this.state.query}
            sort={this.state.sort}
            handleFilter={(query, sort) => this.handleFilter(query, sort)}
            sortOptions={this.props.sortOptions || []}
            filterOptions={this.props.filterOptions || []}
          />);
      } else {
        return (null);
      }
    };

    const enableFilter = () => {
      return this.props.filters !== false;
    };

    const getContent = () => {
      return (
        <div className="paginated-table">
          {(enableFilter()) &&
          <div className="row">
            <div className="col-md-12">
              {getFilters()}
            </div>
          </div>
          }

          <div className="row">
            <div className="col-md-12">
              {this.props.count > 0 && this.props.componentList}
              {!this.props.count && this.props.componentEmpty}
            </div>
          </div>
          {paginate(this.props.count) &&
          <div className="row">
            <Pager>
              <Pager.Item
                onClick={this.handlePreviousPage}
                disabled={!paginatePrevious(this.state.offset)}
              >
                Previous
              </Pager.Item>{' '}
              <Pager.Item
                onClick={this.handleNextPage}
                disabled={!paginateNext(this.state.offset, this.props.count)}
              >
                Next
              </Pager.Item>
            </Pager>
          </div>
          }
        </div>
      );
    };
    return getContent();
  }
}
