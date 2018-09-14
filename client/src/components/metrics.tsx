import * as moment from 'moment';
import * as React from 'react';

import * as Plotly from 'plotly.js';

import * as actions from '../actions/metrics';
import { MetricModel } from '../models/metric';

import Chart from './charts/chart';
import { EmptyList } from './empty/emptyList';
import './metrics.less';

export interface Props {
  metrics: MetricModel[];
  count: number;
  fetchData: () => actions.MetricsAction;
}

export interface DataPoint {
  x: any[];
  y: any[];
}

export default class Metrics extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.fetchData();
  }

  public render() {

    const convertTimeFormat = (d: string) => {
      return moment(d).format('HH:mm:ss');
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
              <div className="metric-item" key={idx}>
                {<Chart data={[data[metricName] as Plotly.PlotData]} title={metricName} />}
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
            <div className="metrics-header">
              Metrics
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-md-10 col-md-offset-1">
            <div className="metrics-content">
              {getMetricComponent()}
            </div>
          </div>
        </div>
      </div>
    );
  }
}
