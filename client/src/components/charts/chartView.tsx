import * as moment from 'moment';
import * as Plotly from 'plotly.js';
import * as React from 'react';

import { Trace } from '../../interfaces/dateTrace';
import { ChartModel } from '../../models/chart';
import { ChartViewModel } from '../../models/chartView';
import { MetricModel } from '../../models/metric';
import Chart from '../charts/chart';

interface Props {
  view: ChartViewModel;
  metrics: MetricModel[];
  className: string;
}

export default class ChartView extends React.Component<Props, {}> {

  public render() {
    const convertTimeFormat = (d: string) => {
      return moment(d).format('YYYY-MM-DD HH:mm:ss');
    };

    const getChartData = (chart: ChartModel) => {
      const traces: { [key: string]: Trace } = {};
      for (const metric of this.props.metrics) {
        const createdAt = metric.created_at;
        for (const metricName of chart.metricNames) {
          if (metricName in traces) {
            traces[metricName].x.push(convertTimeFormat(createdAt));
            traces[metricName].y.push(metric.values[metricName]);
          } else {
            traces[metricName] = {
              x: [convertTimeFormat(createdAt)],
              y: [metric.values[metricName]],
              mode: chart.mode,
              name: metricName
            };
          }
        }
      }
      return chart.metricNames.map((chartName) => traces[chartName]) as Plotly.PlotData[];
    };

    const getChart = (chart: ChartModel) => {
      return (
        <div className={this.props.className}>
          {<Chart data={getChartData(chart)} title={chart.name}/>}
        </div>
      );
    };

    return (
      <div className="row">
        {this.props.view.charts.map((chart) => getChart(chart))}
      </div>
    );
  }
}
