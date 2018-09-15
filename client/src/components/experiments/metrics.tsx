import * as React from 'react';
import { Dropdown, MenuItem } from 'react-bootstrap';

import * as actions from '../../actions/metrics';
import { ChartModel } from '../../models/chart';
import { ChartViewModel } from '../../models/chartView';
import { MetricModel } from '../../models/metric';
import ChartView from '../charts/chartView';

export interface Props {
  metrics: MetricModel[];
  count: number;
  fetchData: () => actions.MetricsAction;
  deleteView?: (view: string) => actions.MetricsAction;
  createView?: (view: string) => actions.MetricsAction;
}

export interface State {
  isGrid: boolean;
  metricNames: string[];
  view: ChartViewModel;
}

export default class Metrics extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    const metricNames = this.getMetricNames();
    this.state = {
      isGrid: true,
      metricNames,
      view: this.getDefaultView(metricNames)
    };
  }

  public componentDidMount() {
    this.props.fetchData();
  }

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (this.props.metrics !== prevProps.metrics) {
      const metricNames = this.getMetricNames();
      this.setState({
        isGrid: prevState.isGrid,
        metricNames,
        view: this.getDefaultView(metricNames)
      });
    }
  }

  public setLayout = () => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      ...{
        isGrid: !this.state.isGrid,
      }
    }));
  };

  public saveView = (event: any) => {
    event.preventDefault();
    if (this.props.createView) {
      this.props.createView('');
    }
    this.handleClose();
  };

  public deleteView = (event: any, view: string) => {
    event.preventDefault();
    if (this.props.deleteView) {
      this.props.deleteView(view);
    }
  };

  public selectView = (view: string) => {
    const state = {};

    this.setState((prevState, prevProps) => ({
      ...prevState, ...state
    }));
  };

  public handleClose = () => {
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{showViewModal: false}
    }));
  };

  public handleShow = () => {
    const saveViewForm = {
      name: '',
    };
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{showViewModal: true, saveViewForm}
    }));
  };

  public getDefaultView = (metricNames: string[]) => {
    const charts: ChartModel[] = [];
    for (const metricName of metricNames) {
      charts.push({name: metricName, metricNames: [metricName], mode: 'lines'} as ChartModel);
    }
    return {charts, name: 'default'} as ChartViewModel;
  };

  public getMetricNames = () => {
    return [...Array.from(
      new Set(([] as string[]).concat(
        ...this.props.metrics.map((metric) => Object.keys(metric.values)))
      )
    )].sort();
  };

  public render() {

    const views: string[] = [];

    const viewsComponent = (
      <Dropdown id="dropdown-views">
        <Dropdown.Toggle
          bsStyle="default"
          bsSize="small"
        >
          <i className="fa fa-clone icon" aria-hidden="true"/> Views
        </Dropdown.Toggle>
        <Dropdown.Menu>
          {views.map(
            (view, idx: number) =>
              <MenuItem
                key={idx}
                className="search-saved-query"
                onClick={() => this.selectView(view)}
              >
                <button
                  type="button"
                  className="close pull-right"
                  aria-label="Close"
                  onClick={(event) => this.deleteView(event, view)}
                >
                  <span aria-hidden="true">&times;</span>
                </button>
                <span>
                      {view || 'untitled'}:
                    </span>
                <p className="query-desc">
                    <span className="label label-search">
                      Query:
                    </span> {view}
                </p>
              </MenuItem>
          )}
          {views.length === 0 &&
          <MenuItem className="search-saved-query">
            No saved views
          </MenuItem>
          }
        </Dropdown.Menu>
      </Dropdown>
    );

    return (
      <div className="metrics">
        <div className="row">
          <div className="col-md-12">
            <div className="btn-group pull-left">
              {viewsComponent}
              <button className="btn btn-sm btn-default" onClick={() => this.handleShow()}>
                <i className="fa fa-download icon" aria-hidden="true"/> Save view
              </button>
            </div>
            <div className="btn-toolbar pull-right">
              <button className="btn btn-sm btn-default">
                <i className="fa fa-plus icon" aria-hidden="true"/> Add chart
              </button>
              <button className="btn btn-sm btn-default" onClick={this.setLayout}>
                {this.state.isGrid
                  ? <span><i className="fa fa-bars icon" aria-hidden="true"/> List</span>
                  : <span><i className="fa fa-th-large icon" aria-hidden="true"/> Grid</span>
                }
              </button>
            </div>
          </div>
          <ChartView
            className={this.state.isGrid ? 'col-md-6' : 'col-md-11 col-md-offset-1'}
            metrics={this.props.metrics}
            view={this.state.view}
          />
        </div>
      </div>
    );
  }
}
