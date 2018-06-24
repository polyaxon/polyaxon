import * as React from 'react';
import { Pager } from 'react-bootstrap';

import { paginate, paginateNext, paginatePrevious } from '../constants/paginate';
import './paginatedList.less';
import FilterList from './filters/filterList';
import ExperimentFilterList from './filters/experimentFilterList';
import { DEFAULT_FILTERS, EXPERIMENT_FILTERS } from './filters/constants';

export interface Props {
  count: number;
  componentList: React.ReactNode;
  componentHeader: React.ReactNode;
  componentEmpty: React.ReactNode;
  filters: boolean | string;
  fetchData: (currentPage: number, query?: string, sort?: string) => any;
}

interface State {
  currentPage: number;
  query?: string;
  sort?: string;
}

export default class PaginatedList extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {currentPage: 1, query: '', sort: ''};
  }

  componentDidMount() {
    this.props.fetchData(this.state.currentPage);
  }

  componentDidUpdate(prevProps: Props, prevState: State) {
    let changed = false;
    if (this.state.currentPage !== prevState.currentPage) {
      changed = true;
    }
    if (this.state.query !== prevState.query) {
      changed = true;
    }
    if (this.state.sort !== prevState.sort) {
      changed = true;
    }
    if (changed) {
      this.props.fetchData(this.state.currentPage, this.state.query, this.state.sort);
    }
  }

  handleNextPage = () => {
    this.setState((prevState, prevProps) => ({
      currentPage: prevState.currentPage + 1,
    }));
  }

  handlePreviousPage = () => {
    this.setState((prevState, prevProps) => ({
      currentPage: prevState.currentPage - 1,
    }));
  }

  handleFilter = (query: string, sort: string) => {
    this.setState((prevState, prevProps) => ({
      query: query,
      sort: sort
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
            handleFilter={(query, sort) => this.handleFilter(query, sort)}
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
          {(this.props.count > 0 && enableFilter()) &&
          <div className="row">
            <div className="col-md-12">
              {getFilters()}
            </div>
          </div>
          }
          <div className="row">
            <div className="col-md-12">
              <div className="list-header">
                {this.props.componentHeader}
              </div>
            </div>
          </div>
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
                disabled={!paginatePrevious(this.state.currentPage)}
              >
                Previous
              </Pager.Item>{' '}
              <Pager.Item
                onClick={this.handleNextPage}
                disabled={!paginateNext(this.state.currentPage, this.props.count)}
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
