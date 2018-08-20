import * as React from 'react';

import './filterList.less';

export interface Props {
  query?: string;
  sort?: string;
  extraFilters?: {[key: string]: number|boolean|string};
  handleFilter: (query: string,
                 sort: string,
                 extraFilters?: {[key: string]: number|boolean|string}) => any;
}

interface State {
  query: string;
  sort: string;
  dataRadio?: string;
  independent?: boolean;
  showFilters?: boolean;
}

export default class ExperimentFilterList extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    let dataRadio = 'info';
    let independent = false;
    if (props.extraFilters &&
        (props.extraFilters.metrics === true || props.extraFilters.metrics === 'true')) {
      dataRadio = 'metrics';
    }
    if (props.extraFilters &&
        (props.extraFilters.declarations === true || props.extraFilters.declarations === 'true')) {
      dataRadio = 'declarations';
    }
    if (props.extraFilters &&
        (props.extraFilters.independent === true || props.extraFilters.independent === 'true')) {
      independent = true;
    }
    this.state = {
      query: props.query || '',
      sort: props.sort || '',
      dataRadio,
      independent,
      showFilters: false
    };
  }

  public handleFilter = (event: any) => {
    event.preventDefault();
    const extraFilters: {[key: string]: number|boolean|string} = {};
    if (this.state.dataRadio === 'metrics') {
      extraFilters.metrics = true;
    } else if (this.state.dataRadio === 'declarations') {
      extraFilters.declarations = true;
    }

    if (this.state.independent === true) {
      extraFilters.independent = true;
    }

    this.props.handleFilter(this.state.query, this.state.sort, extraFilters);
  }

  public onQueryInput = (value: string) => {
    this.setState((prevState, prevProps) => ({
      query: value,
      sort: prevState.sort,
    }));
  }

  public onSortInput = (value: string) => {
    this.setState((prevState, prevProps) => ({
      query: prevState.query,
      sort: value,
    }));
  }

  public onIndependentInput = (value: string) => {
    this.setState((prevState, prevProps) => ({
      query: prevState.query,
      sort: prevState.sort,
      independent: !prevState.independent
    }));
  }

  public onDataRadioChange = (value: string) => {
    this.setState((prevState, prevProps) => ({
      query: prevState.query,
      sort: prevState.sort,
      dataRadio: value
    }));
  }

  public onHideFilters = () => {
    this.setState((prevState, prevProps) => ({
      showFilters: !prevState.showFilters
    }));
  }

  public render() {
    const getFilter = () => {
      return (
        <div className="filter-list">
            <div className="col-md-offset-10 col-md-2">
              <div className="col-md-offset-2 col-md-10">
              <button
                className="btn btn-default btn-filters"
                onClick={this.onHideFilters}
              >
                <i className="fa fa-sliders icon" aria-hidden="true"/>
              </button>
              </div>
          </div>
          {this.state.showFilters &&
          <form className="form-horizontal" onSubmit={this.handleFilter}>
            <div className="col-md-10">
              <div className="form-group">
                <label htmlFor="query" className="col-md-1 control-label">Query</label>
                <div className="col-md-11">
                  <input
                    type="text"
                    className="form-control"
                    id="query"
                    placeholder="metrics.loss:<=0.1, status:~running|scheduled, created_at:2018-01-01..2018-02-01"
                    value={this.state.query}
                    onChange={(event) => this.onQueryInput(event.target.value)}
                  />
                </div>
              </div>
              <div className="form-group">
                <label htmlFor="query" className="col-md-1 control-label">Sort</label>
                <div className="col-md-11">
                  <input
                    type="text"
                    className="form-control"
                    id="sort"
                    placeholder="-started_at, -metric.accuracy"
                    value={this.state.sort}
                    onChange={(event) => this.onSortInput(event.target.value)}
                  />
                </div>
              </div>
              <div className="form-group">
                <label htmlFor="query" className="col-md-1 control-label">Independent</label>
                <div className="col-md-2">
                  <label className="switch">
                    <input
                      type="checkbox"
                      defaultChecked={this.state.independent}
                      onChange={(event) => this.onIndependentInput(event.target.value)}
                    />
                    <span className="slider round"/>
                  </label>
                </div>
              </div>
              <div className="form-group">
                <div className="col-md-offset-1 col-md-1">
                  <div className="radio">
                    <label>
                      <input
                        type="radio"
                        value="info"
                        checked={this.state.dataRadio === 'info'}
                        onChange={(event) => this.onDataRadioChange(event.target.value)}
                      /> Info
                    </label>
                  </div>
                </div>
                <div className="col-md-1">
                  <div className="radio">
                    <label>
                      <input
                        type="radio"
                        value="metrics"
                        checked={this.state.dataRadio === 'metrics'}
                        onChange={(event) => this.onDataRadioChange(event.target.value)}
                      /> Metrics
                    </label>
                  </div>
                </div>
                <div className="col-md-1">
                  <div className="radio">
                    <label>
                      <input
                        type="radio"
                        value="declarations"
                        checked={this.state.dataRadio === 'declarations'}
                        onChange={(event) => this.onDataRadioChange(event.target.value)}
                      /> Declarations
                    </label>
                  </div>
                </div>
              </div>
            </div>
            <div className="filter-buttons col-md-1">
              <div className="form-group">
                <div className="col-md-offset-2 col-md-10">
                  <button type="submit" className="btn btn-primary">Search</button>
                </div>
              </div>
            </div>
          </form>
          }
        </div>
      );
    };

    return getFilter();
  }
}
