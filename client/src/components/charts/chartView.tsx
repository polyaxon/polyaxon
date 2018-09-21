import * as moment from 'moment';
import * as Plotly from 'plotly.js';
import * as React from 'react';

import { CHARTS_COLORS } from '../../constants/charts';
import { Trace } from '../../interfaces/dateTrace';
import { ChartModel, ChartTypes, TraceModes, TraceTypes } from '../../models/chart';
import { ChartViewModel } from '../../models/chartView';
import { MetricModel } from '../../models/metric';
import Chart from '../charts/chart';

import './chart.less';

interface Props {
  view: ChartViewModel;
  metrics: MetricModel[];
  resource: string;
  className: string;
  onRemoveChart: (chartIdx: number) => void;
}

export default class ChartView extends React.Component<Props, {}> {

  public render() {
    const convertTimeFormat = (d: string) => {
      return moment(d).format('YYYY-MM-DD HH:mm:ss');
    };

    const getTraceMode = (chartType: ChartTypes): TraceModes => {
      if (chartType === 'line') {
        return 'lines';
      } else if (chartType === 'bar') {
        return 'none';
      } else if (chartType === 'scatter') {
        return 'markers';
      }
      return 'lines';
    };

    const getTraceType = (chartType: ChartTypes): TraceTypes => {
      if (chartType === 'line') {
        return 'scatter';
      } else if (chartType === 'bar') {
        return 'bar';
      } else if (chartType === 'scatter') {
        return 'scatter';
      }
      return 'scatter';
    };

    const getTraceName = (metricName: string, prefix?: string | number) => {
      return prefix ? `${prefix}.${metricName}` : metricName;
    };

    const getchartYData = (metric: MetricModel, chart: ChartModel, prefix: string) => {
      const dataTraces: { [key: string]: Plotly.Datum[] } = {};
      chart.metricNames.forEach((metricName, idx) => {
        const traceName = getTraceName(metricName, prefix);
        if (traceName in dataTraces) {
          dataTraces[traceName].push(metric.values[metricName]);
        } else {
          dataTraces[traceName] = [metric.values[metricName]];
        }
      });

      return dataTraces;
    };

    const getchartXData = (metric: MetricModel, chart: ChartModel, prefix: string) => {
      const dataTraces: { [key: string]: Plotly.Datum[] } = {};
      let xValue: number | string;
      if (this.props.view.meta.xAxis === 'step' && 'step' in metric.values) {
        xValue = metric.values.step;
      } else {
        xValue = convertTimeFormat(metric.created_at);
      }

      chart.metricNames.forEach((metricName, idx) => {
        const traceName = getTraceName(metricName, prefix);
        if (traceName in dataTraces) {
          dataTraces[traceName].push(xValue);
        } else {
          dataTraces[traceName] = [xValue];
        }
      });

      return dataTraces;
    };

    const getTraces = (chart: ChartModel) => {
      const traces: { [key: string]: Trace } = {};
      const traceNames: string[] = [];
      for (const metric of this.props.metrics) {
        let prefix = '';
        if (this.props.resource === 'groups') {
          prefix = `${metric.experiment}`;
        }
        let xValue: number | string;
        if (this.props.view.meta.xAxis === 'step' && 'step' in metric.values) {
          xValue = metric.values.step;
        } else {
          xValue = convertTimeFormat(metric.created_at);
        }
        chart.metricNames.forEach((metricName, idx) => {
          const traceName = getTraceName(metricName, prefix);
          if (traceName in traces) {
            traces[traceName].x.push(xValue);
            traces[traceName].y.push(metric.values[metricName]);
          } else {
            traceNames.push(traceName);
            traces[traceName] = {
              x: [xValue],
              y: [metric.values[metricName]],
              name: traceName,
              mode: getTraceMode(chart.type),
              type: getTraceType(chart.type),
            };
          }
        });
      }
      return traceNames
        .map((traceName, idx) => {
          const trace = traces[traceName];
          if (trace.type === 'scatter') {
            if (trace.x.length === 1) {
              trace.type = 'bar';
            } else {
              trace.line = {
                width: 1.7,
                shape: 'spline',
                smoothing: this.props.view.meta.smoothing,
                color: CHARTS_COLORS[idx % CHARTS_COLORS.length],
              } as Partial<Plotly.ScatterLine>;
            }
          }
          if (trace.type === 'bar') {
            trace.marker = {color: CHARTS_COLORS[idx % CHARTS_COLORS.length]};
            if (trace.x.length > 1) {
              trace.x = [trace.x[trace.x.length - 1]];
              trace.y = [trace.y[trace.y.length - 1]];
            }
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
            {<Chart data={getTraces(chart)}/>}
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
