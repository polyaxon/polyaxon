import * as React from 'react';

import './filterList.less';

export interface Props {
  query?: string;
  sort?: string;
  radio?: string;
  handleFilter: (query: string, sort: string) => any;
}

interface State {
  query: string;
  sort: string;
  radio: string;
}

export default class FilterList extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {query: props.query || '', sort: props.sort || '', radio: 'data'};
  }

  handleFilter = (event: any) => {
    event.preventDefault();
    this.props.handleFilter(this.state.query, this.state.sort);
  }

  onQueryInput = (value: string) => {
    this.setState((prevState, prevProps) => ({
      query: value,
      sort: prevState.sort,
      radio: prevState.radio
    }));
  }

  onSortInput = (value: string) => {
    this.setState((prevState, prevProps) => ({
      query: prevState.query,
      sort: value,
      radio: prevState.radio
    }));
  }

  onRadioChange = (value: string) => {
    this.setState((prevState, prevProps) => ({
      query: prevState.query,
      sort: prevState.sort,
      radio: value
    }));
  }

  public render() {
    let getFilter = () => {
      return (
        <div className="filter-list">
          {/*<div className="sort sliders-h"></div>*/}
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
                    onChange={(event) =>  this.onQueryInput(event.target.value)}
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
                <div className="col-md-offset-1 col-md-1">
                  <div className="radio">
                    <label>
                      <input
                        type="radio"
                        value="data"
                        checked={this.state.radio === 'data'}
                        onChange={(event) => this.onRadioChange(event.target.value)}
                      /> Data
                    </label>
                  </div>
                </div>
                <div className="col-md-1">
                  <div className="radio">
                    <label>
                      <input
                        type="radio"
                        value="metrics"
                        checked={this.state.radio === 'metrics'}
                        onChange={(event) => this.onRadioChange(event.target.value)}
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
                        checked={this.state.radio === 'declarations'}
                        onChange={(event) => this.onRadioChange(event.target.value)}
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
        </div>
      );
    };

    return getFilter();
  }
}
