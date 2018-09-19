import * as moment from 'moment';
import * as Plotly from 'plotly.js';
import * as React from 'react';

import { CHARTS_COLORS } from '../../constants/charts';
import { Trace } from '../../interfaces/dateTrace';
import { ChartModel } from '../../models/chart';
import { ChartViewModel } from '../../models/chartView';
import { MetricModel } from '../../models/metric';
import Chart from '../charts/chart';

import './chart.less';

interface Props {
  view: ChartViewModel;
  metrics: MetricModel[];
  className: string;
  onRemoveChart: (chartIdx: number) => void;
}

export default class ChartView extends React.Component<Props, {}> {

  public render() {
    const convertTimeFormat = (d: string) => {
      return moment(d).format('YYYY-MM-DD HH:mm:ss');
    };

    const getChartData = (chart: ChartModel) => {
      const traces: { [key: string]: Trace } = {};
      for (const metric of this.props.metrics) {
        let xValue: number|string;
        if (this.props.view.meta.xAxis === 'step' && 'step' in metric.values) {
          xValue = metric.values.step;
        } else {
          xValue = convertTimeFormat(metric.created_at);
        }
        chart.metricNames.forEach((metricName, idx) => {
          if (metricName in traces) {
            traces[metricName].x.push(xValue);
            traces[metricName].y.push(metric.values[metricName]);
          } else {
            traces[metricName] = {
              x: [xValue],
              y: [metric.values[metricName]],
              name: metricName,
              mode: chart.mode,
              type: chart.type,
              marker: {color: CHARTS_COLORS[idx % CHARTS_COLORS.length]},
              line: {
                width: 0.8,
                shape: 'spline',
                smoothing: this.props.view.meta.smoothing,
                color: CHARTS_COLORS[idx % CHARTS_COLORS.length],
              } as Partial<Plotly.ScatterLine>
            };
          }
        });
      }
      return chart.metricNames
        .filter((chartName) => chartName in traces)
        .map((chartName) => {
          const trace = traces[chartName];
          if (trace.x.length === 1 && trace.type === 'scatter') {
            trace.type = 'bar';
          }
          return trace;
        }) as Plotly.PlotData[];
    };

    const getChart = (chart: ChartModel, idx: number) => {
      return (
        <div className={this.props.className + ' chart-item'} key={chart.name + idx}>
          <div className="chart">
            <h5 className="chart-header">{chart.name}
              <button
                className="btn btn-sm btn-default pull-right"
                onClick={() => this.props.onRemoveChart(idx)}
              >Remove
              </button>
            </h5>
            {<Chart data={getChartData(chart)}/>}
          </div>
        </div>
      );
    };

    return (
      <div className="row">
        {this.props.view.charts.map((chart, idx) => getChart(chart, idx))}
      </div>
    );
  }
}
