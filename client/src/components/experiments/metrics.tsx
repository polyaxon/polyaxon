import * as moment from 'moment';
import * as React from 'react';
import { Dropdown, MenuItem } from 'react-bootstrap';

import * as Plotly from 'plotly.js';

import * as actions from '../../actions/metrics';
import { DataPoint } from '../../interfaces/dataPoint';
import { MetricModel } from '../../models/metric';
import Chart from '../charts/chart';
import { EmptyList } from '../empty/emptyList';

export interface Props {
  metrics: MetricModel[];
  count: number;
  fetchData: () => actions.MetricsAction;
  deleteView?: (view: string) => actions.MetricsAction;
  createView?: (view: string) => actions.MetricsAction;
}

export interface State {
  isGrid: boolean;
}

export default class Metrics extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      isGrid: true,
    };
  }

  public componentDidMount() {
    this.props.fetchData();
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

  public render() {

    const convertTimeFormat = (d: string) => {
      return moment(d).format('YYYY-MM-DD HH:mm:ss');
    };

    const metricNames = [...Array.from(
      new Set(([] as string[]).concat(
        ...this.props.metrics.map((metric) => Object.keys(metric.values)))
      )
    )].sort();
    const views: string[] = [];

    const getMetricComponentData = () => {
      const metrics = this.props.metrics;
      const metricData: { [key: string]: DataPoint } = {};

      for (const metric of metrics) {
        const createdAt = metric.created_at;
        for (const metricName of Object.keys(metric.values)) {
          if (metricName in metricData) {
            metricData[metricName].x.push(convertTimeFormat(createdAt));
            metricData[metricName].y.push(metric.values[metricName]);
          } else {
            metricData[metricName] = {
              x: [convertTimeFormat(createdAt)],
              y: [metric.values[metricName]]
            };
          }
        }
      }

      return metricData;
    };

    const getMetricComponent = () => {
      if (this.props.count === 0) {
        return EmptyList(false, 'metric', 'metric');
      } else {
        const data = getMetricComponentData();
        return Object.keys(data).map(
          (metricName, idx) => {
            return (
              <div
                className={this.state.isGrid ? 'col-md-6' : 'col-md-11 col-md-offset-1'}
                key={idx}
              >
                {<Chart data={[data[metricName] as Plotly.PlotData]} title={metricName}/>}
              </div>
            );
          }
        );
      }
    };

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
          <div className="row">
            {getMetricComponent()}
          </div>
        </div>
      </div>
    );
  }
}
