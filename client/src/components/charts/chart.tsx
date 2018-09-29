import * as React from 'react';

import * as Plotly from 'plotly.js';

import { ChartTypes } from '../../models/chart';
import PlotlyChart from './plotlyChart';

interface Props {
  data: Plotly.PlotData[];
  layout: Plotly.Layout;
  config: Plotly.Config;
  chartType: ChartTypes;
  title?: string;
}

export default class Chart extends React.Component<Props, {}> {
  public render() {
    return (
      <PlotlyChart
        data={this.props.data}
        layout={this.props.layout}
        config={this.props.config}
      />
    );
  }
}
