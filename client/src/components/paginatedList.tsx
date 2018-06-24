import * as React from 'react';
import { Pager } from 'react-bootstrap';

import * as deepEqual from 'deep-equal';
import * as queryString from 'query-string';

import { PAGE_SIZE, paginate, paginateNext, paginatePrevious } from '../constants/paginate';
import './paginatedList.less';
import FilterList from './filters/filterList';
import ExperimentFilterList from './filters/experimentFilterList';
import { DEFAULT_FILTERS, EXPERIMENT_FILTERS } from './filters/constants';

export interface Props {
  count: number;
  componentList: React.ReactNode;
  componentHeader?: React.ReactNode;
  componentEmpty: React.ReactNode;
  filters: boolean | string;
  fetchData: (offset: number, query?: string, sort?: string, extraFilters?: Object) => any;
}

interface State {
  offset: number;
  query?: string;
  sort?: string;
  extraFilters?: {[key: string]: number|boolean|string};
}

export default class PaginatedList extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = this.getFilters();
  }

  getFilters() {
    let filters = {offset: 0, query: '', sort: '', extraFilters: {}};
    let pieces = location.href.split('?');
    if (pieces.length > 1) {
      let search = queryString.parse(pieces[1]);
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

  componentDidMount() {
    this.props.fetchData(
        this.state.offset,
        this.state.query,
        this.state.sort,
        this.state.extraFilters);
  }

  componentDidUpdate(prevProps: Props, prevState: State) {
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

  handleNextPage = () => {
    this.setState((prevState, prevProps) => ({
      offset: prevState.offset + PAGE_SIZE,
    }));
  }

  handlePreviousPage = () => {
    this.setState((prevState, prevProps) => ({
      offset: prevState.offset - PAGE_SIZE,
    }));
  }

  handleFilter = (query: string, sort: string, extraFilters?: {[key: string]: number|boolean|string}) => {
    this.setState((prevState, prevProps) => ({
      query: query,
      sort: sort,
      extraFilters: extraFilters,
    }));
  }

  public render() {
    let getFilters = () => {
      if (this.props.filters === DEFAULT_FILTERS) {
        return (
          <FilterList
            query={this.state.query}
            sort={this.state.sort}
            handleFilter={(query, sort) => this.handleFilter(query, sort)}
          />);
      } else if (this.props.filters === EXPERIMENT_FILTERS) {
        return (
          <ExperimentFilterList
            query={this.state.query}
            sort={this.state.sort}
            extraFilters={this.state.extraFilters}
            handleFilter={(query, sort, extraFilters) => this.handleFilter(query, sort, extraFilters)}
          />
        );
      } else {
        return (null);
      }
    };

    let enableFilter = () => {
      return this.props.filters !== false;
    };

    let getContent = () => {
      return (
        <div className="paginated-list">
          {(enableFilter()) &&
          <div className="row">
            <div className="col-md-12">
              {getFilters()}
            </div>
          </div>
          }
          {this.props.componentHeader &&
          <div className="row">
            <div className="col-md-12">
              <div className="list-header">
                {this.props.componentHeader}
              </div>
            </div>
          </div>
          }
          {this.props.count > 0 &&
          <div className="row">
            <div className="col-md-12">
              <div className="list-items">
                {this.props.componentList}
              </div>
            </div>
          </div>}
          {!this.props.count && this.props.componentEmpty}
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
