import * as React from 'react';
import { Dropdown, MenuItem } from 'react-bootstrap';

import './filterList.less';

export interface Props {
  query?: string;
  sort?: string;
  handleFilter: (query: string, sort: string) => any;
  sortOptions: string[];
  defaultSort?: string;
}

interface State {
  query: string;
  sort: string;
  showFilters: boolean;
}

export default class FilterList extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      query: props.query || '',
      sort: props.sort || props.defaultSort ||  '-updated_at',
      showFilters: false
    };
  }

  public handleFilter = (event: any) => {
    event.preventDefault();
    this.props.handleFilter(this.state.query, this.state.sort);
  };

  public onQueryInput = (value: string) => {
    this.setState((prevState, prevProps) => ({
      query: value,
      sort: prevState.sort,
    }));
  };

  public onSortInput = (value: string) => {
    this.setState((prevState, prevProps) => ({
      query: prevState.query,
      sort: value,
    }));
    this.props.handleFilter(this.state.query, value);
  };

  public render() {
    const getFilter = () => {
      return (
        <div className="filter-list">
          <form onSubmit={this.handleFilter}>
            <div className="form-group search-group">
              <div className="input-group search-query">
                <span className="input-group-btn">
                  <Dropdown id={`dropdown-actions-1`} className="search-history">
                    <Dropdown.Toggle
                      bsStyle="default"
                      bsSize="small"
                      noCaret={true}
                    >
                      <i className="fa fa-search icon" aria-hidden="true"/> Searches
                    </Dropdown.Toggle>
                    <Dropdown.Menu>
                      <MenuItem eventKey="2">
                        item
                      </MenuItem>
                    </Dropdown.Menu>
                  </Dropdown>
                </span>
                <input
                  type="text"
                  className="form-control input-sm"
                  id="query"
                  placeholder="build.id:3|4, status:~running|scheduled, created_at:2018-01-01..2018-02-01"
                  value={this.state.query}
                  onChange={(event) => this.onQueryInput(event.target.value)}
                />
                <span className="input-group-btn">
                  <button
                    type="button"
                    className="btn btn-default btn-sm btn-search"
                    aria-label="Help"
                  >
                    <i className="fa fa-plus icon" aria-hidden="true"/>
                  </button>
                </span>
              </div>
              <Dropdown
                id={`dropdown-actions-1`}
                pullRight={true}
                className="search-sort"
              >
                <Dropdown.Toggle
                  bsStyle="default"
                  bsSize="small"
                  noCaret={true}
                >
                  <i className="fa fa-sort icon" aria-hidden="true"/> {`Sort by: ${this.state.sort}`}
                </Dropdown.Toggle>
                <Dropdown.Menu>
                  {this.props.sortOptions.map((sortOption: string) =>
                  <MenuItem
                    key={sortOption}
                    eventKey="2"
                    onClick={() => this.onSortInput(this.state.sort === sortOption ? `-${sortOption}` : sortOption)}
                  >
                    {this.state.sort === sortOption &&
                    <i className="fa fa-long-arrow-up icon" aria-hidden="true"/>
                    }{this.state.sort === `-${sortOption}` &&
                    <i className="fa fa-long-arrow-down icon" aria-hidden="true"/>} {sortOption}
                  </MenuItem>
                  )}
                </Dropdown.Menu>
              </Dropdown>
            </div>
          </form>
        </div>
      );
    };

    return getFilter();
  }
}
