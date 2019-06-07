import * as React from 'react';
import { Dropdown, MenuItem, Modal } from 'react-bootstrap';

import * as actions from '../../actions/search';
import FilterCreate from '../../containers/filters/filterCreate';
import { ColumnInterface } from '../../interfaces/tableColumns';
import { SearchModel } from '../../models/search';
import { DefaultSearches } from './filterDefault';

import '../dropdowns.less';
import './filterList.less';

export interface Props {
  query?: string;
  sort?: string;
  handleFilter: (query: string, sort: string) => any;
  sortOptions: string[];
  columnOptions: ColumnInterface[];
  defaultSort?: string;
  fetchSearches?: () => actions.SearchAction;
  createSearch?: (data: SearchModel) => actions.SearchAction;
  deleteSearch?: (searchId: number) => actions.SearchAction;
  selectSearch?: (data: SearchModel) => void;
  searches: SearchModel[];
  searchesCount: number;
}

interface State {
  query: string;
  sort: string;
  showFilters: boolean;
  showSearchModal: boolean;
  saveQueryForm: { name: string, query: string, sort: string };
}

export default class FilterList extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      query: props.query || '',
      sort: props.sort || props.defaultSort || '-updated_at',
      showFilters: false,
      showSearchModal: false,
      saveQueryForm: {
        query: '',
        sort: '',
        name: '',
      }
    };
  }

  public componentDidMount() {
    if (this.props.fetchSearches) {
      this.props.fetchSearches();
    }
  }

  public handleFilter = (event: any) => {
    event.preventDefault();
    this.props.handleFilter(this.state.query, this.state.sort);
  };

  public saveSearch = (form: { name: string, query: string, sort: string }) => {
    if (this.props.createSearch) {
      this.props.createSearch({
        id: -1,
        name: form.name,
        query: {
          query: form.query,
          sort: form.sort
        }
      });
    }
  };

  public deleteSearch = (event: any, search: SearchModel) => {
    event.preventDefault();
    if (this.props.deleteSearch) {
      this.props.deleteSearch(search.id);
    }
  };

  public selectSearch = (search: SearchModel) => {
    const state = {
      query: search.query.query,
      sort: search.query.sort || this.props.defaultSort || '-updated_at',
    };

    if (this.props.selectSearch) {
      this.props.selectSearch(search);
    }

    this.setState((prevState, prevProps) => ({
      ...prevState, ...state
    }));

    this.props.handleFilter(state.query, state.sort);
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

  public handleClose = () => {
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{showSearchModal: false}
    }));
  };

  public handleShow = () => {
    const saveQueryForm = {
      query: this.state.query,
      sort: this.state.sort,
      name: '',
      meta: {}
    };
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{showSearchModal: true, saveQueryForm}
    }));
  };

  public updateQueryForm = (key: string, value: string) => {
    const saveQueryForm = {...this.state.saveQueryForm};
    if (key === 'name') {
      saveQueryForm.name = value;
    } else if (key === 'query') {
      saveQueryForm.query = value;
    } else if (key === 'sort') {
      saveQueryForm.sort = value;
    }
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{saveQueryForm}
    }));
  };

  public render() {
    const getFilter = () => {
      return (
        <div className="filter-list">
          <form onSubmit={this.handleFilter}>
            <div className="form-group search-group">
              <div className="search-form">
                <div className="input-group search-query">
                  {this.props.fetchSearches &&
                  <span className="input-group-btn">
                  <Dropdown id="dropdown-searches" className="saved-searches">
                    <Dropdown.Toggle
                      bsStyle="default"
                      bsSize="small"
                    >
                      <i className="fas fa-history icon" aria-hidden="true"/> Searches
                    </Dropdown.Toggle>
                    <Dropdown.Menu className="dropdown-menu-large">
                      {DefaultSearches.map(
                        (search: SearchModel, idx: number) =>
                          <MenuItem
                            key={`d-${idx}`}
                            className="dropdown-select-menu"
                            onClick={() => this.selectSearch(search)}
                          >
                            <span className="dropdown-title dropdown-title-label">
                              {search.name || 'untitled'}
                            </span>
                            <p className="dropdown-meta">
                              <span className="label dropdown-label">
                                Query:
                              </span> {search.query.query && search.query.query}
                              <span className="label dropdown-label">
                                Sort:
                              </span> {search.query.sort || this.props.defaultSort || '-update_at'}
                            </p>
                          </MenuItem>
                      )}
                      {this.props.searches.map(
                        (search: SearchModel, idx: number) =>
                          <MenuItem
                            key={idx}
                            className="dropdown-select-menu"
                            onClick={() => this.selectSearch(search)}
                          >
                            <button
                              type="button"
                              className="close pull-right"
                              aria-label="Close"
                              onClick={(event) => this.deleteSearch(event, search)}
                            >
                              <span aria-hidden="true">&times;</span>
                            </button>
                            <span className="dropdown-title">
                              {search.name || 'untitled'}
                            </span>
                            <p className="dropdown-meta">
                              <span className="label dropdown-label">
                                Query:
                              </span> {search.query.query && search.query.query}
                              <span className="label dropdown-label">
                                Sort:
                              </span> {search.query.sort || this.props.defaultSort || '-update_at'}
                            </p>
                          </MenuItem>
                      )}
                      <MenuItem className="searches-save" onClick={() => this.handleShow()}>
                        <i
                          className={'fas fa-search-plus icon'}
                          aria-hidden="true"
                        /> Save current search
                      </MenuItem>
                    </Dropdown.Menu>
                  </Dropdown>
                </span>
                  }
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
                    id="dropdown-add"
                    pullRight={true}
                    className="search-add"
                  >
                    <Dropdown.Toggle
                      bsStyle="default"
                      bsSize="small"
                      noCaret={true}
                    >
                      <i className="fas fa-chevron-down icon" aria-hidden="true"/>
                    </Dropdown.Toggle>
                    <Dropdown.Menu className="dropdown-menu-large">
                      {this.props.columnOptions.map(
                        (filterOption: ColumnInterface, idx: number) =>
                          <MenuItem
                            key={`f-${idx}`}
                            className="search-filter"
                            onClick={() => this.addFilter(filterOption.field)}
                          >
                              <span>
                                <i
                                  className={filterOption.icon + ' icon'}
                                  aria-hidden="true"
                                /> {filterOption.field}
                              </span>
                            <p className="filter-desc">{filterOption.desc}</p>
                          </MenuItem>
                      )}
                      <MenuItem href="https://docs.polyaxon.com/references/polyaxon-query-syntax/" target="_blank">
                        <i className="fas fa-external-link-alt icon" aria-hidden="true"/> View advanced search syntax
                      </MenuItem>
                    </Dropdown.Menu>
                  </Dropdown>
                  <button
                    type="button"
                    className="btn btn-default btn-sm btn-search"
                    aria-label="Help"
                    onClick={this.handleFilter}
                  >
                    <i className="fas fa-search icon" aria-hidden="true"/>
                  </button>
                </span>
                </div>
              </div>
              <Dropdown
                id="dropdown-sort"
                pullRight={true}
                className="search-sort"
              >
                <Dropdown.Toggle
                  bsStyle="default"
                  bsSize="small"
                  noCaret={true}
                >
                  <i className="fas fa-sort icon" aria-hidden="true"/> {`Sort by: ${this.state.sort}`}
                </Dropdown.Toggle>
                <Dropdown.Menu className="dropdown-menu-large">
                  {this.props.sortOptions.map((sortOption: string) =>
                    <MenuItem
                      key={sortOption}
                      onClick={() => this.onSortInput(this.state.sort === sortOption ? `-${sortOption}` : sortOption)}
                    >
                      {this.state.sort === sortOption &&
                      <i className="fas fa-sort-amount-up icon" aria-hidden="true"/>
                      }{this.state.sort === `-${sortOption}` &&
                    <i className="fas fa-sort-amount-down icon" aria-hidden="true"/>} {sortOption}
                    </MenuItem>
                  )}
                </Dropdown.Menu>
              </Dropdown>
            </div>
          </form>
          <Modal show={this.state.showSearchModal} onHide={this.handleClose}>
            <Modal.Header closeButton={true}>
              <Modal.Title>Save search query</Modal.Title>
            </Modal.Header>
            <Modal.Body>
              <FilterCreate
                onCreate={this.saveSearch}
                onClose={this.handleClose}
                name=""
                query={this.state.query}
                sort={this.state.sort}
              />
            </Modal.Body>
          </Modal>
        </div>
      );
    };

    return getFilter();
  }
}
