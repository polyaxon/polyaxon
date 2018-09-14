import * as moment from 'moment';
import * as React from 'react';

import * as Plotly from 'plotly.js';

import * as actions from '../actions/metrics';
import { MetricModel } from '../models/metric';

import Chart from './charts/chart';
import { EmptyList } from './empty/emptyList';

export interface Props {
  metrics: MetricModel[];
  count: number;
  fetchData: () => actions.MetricsAction;
}

export interface DataPoint {
  x: Plotly.Datum[];
  y: Plotly.Datum[];
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

  public render() {

    const convertTimeFormat = (d: string) => {
      return moment(d).format('YYYY-MM-DD HH:mm:ss');
    };

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
                className={this.state.isGrid ? 'col-md-11 col-md-offset-1' : 'col-md-6'}
                key={idx}
              >
                {<Chart data={[data[metricName] as Plotly.PlotData]} title={metricName}/>}
              </div>
            );
          }
        );
      }
    };

    return (
      <div className="metrics">
        <div className="row">
          <div className="col-md-12">
            <div className="btn-toolbar pull-left">
              <button className="btn btn-sm btn-default" onClick={this.setLayout}>
                <i className="fa fa-save icon" aria-hidden="true"/> Save
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
