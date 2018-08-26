import * as React from 'react';
import { Dropdown, MenuItem } from 'react-bootstrap';

import { FilterOption } from '../../interfaces/filterOptions';
import './filterList.less';

export interface Props {
  query?: string;
  sort?: string;
  handleFilter: (query: string, sort: string) => any;
  sortOptions: string[];
  filterOptions: FilterOption[];
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
      sort: props.sort || props.defaultSort || '-updated_at',
      showFilters: false
    };
  }

  public handleFilter = (event: any) => {
    event.preventDefault();
    this.props.handleFilter(this.state.query, this.state.sort);
  };

  public onQueryInput = (query: string) => {
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{query}
    }));
  };

  public onSortInput = (sort: string) => {
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{sort}
    }));
    this.props.handleFilter(this.state.query, sort);
  };

  public addFilter = (filter: string) => {
    const query = this.state.query ? this.state.query + ', ' + filter + ': ' : filter + ': ';
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{query}
    }));
  };

  public render() {
    const getFilter = () => {
      return (
        <div className="filter-list">
          <form onSubmit={this.handleFilter}>
            <div className="form-group search-group">
              <div className="input-group search-query">
                <span className="input-group-btn">
                  <Dropdown id={`dropdown-searches`}>
                    <Dropdown.Toggle
                      bsStyle="default"
                      bsSize="small"
                    >
                      <i className="fa fa-history icon" aria-hidden="true"/> Searches
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
                  <Dropdown
                    id={`dropdown-add`}
                    pullRight={true}
                    className="search-add"
                  >
                    <Dropdown.Toggle
                      bsStyle="default"
                      bsSize="small"
                      noCaret={true}
                    >
                      <i className="fa fa-chevron-down icon" aria-hidden="true"/>
                    </Dropdown.Toggle>
                    <Dropdown.Menu>
                      {this.props.filterOptions.map(
                        (filterOption: FilterOption, idx: number) =>
                          <MenuItem
                            key={idx}
                            className="search-filter"
                            onClick={() => this.addFilter(filterOption.filter)}
                          >
                            <span>
                              <i
                                className={'fa fa-' + filterOption.icon + ' icon'}
                                aria-hidden="true"
                              /> {filterOption.filter}
                            </span>
                            <p className="filter-desc">{filterOption.desc}</p>
                          </MenuItem>
                      )}
                      <MenuItem href="https://docs.polyaxon.com/query_syntax/introduction" target="_blank">
                        <i className="fa fa-external-link icon" aria-hidden="true"/> View advanced search syntax
                      </MenuItem>
                    </Dropdown.Menu>
                  </Dropdown>
                  <button
                    type="button"
                    className="btn btn-default btn-sm btn-search"
                    aria-label="Help"
                    onClick={this.handleFilter}
                  >
                    <i className="fa fa-search icon" aria-hidden="true"/>
                  </button>
                </span>
              </div>
              <Dropdown
                id={`dropdown-sort`}
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
