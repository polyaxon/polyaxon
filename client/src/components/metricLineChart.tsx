import * as React from 'react';
import { LineChart, XAxis, Tooltip, CartesianGrid, Line, YAxis, ResponsiveContainer, Legend } from 'recharts';
import { CHARTS_COLORS } from '../constants/charts';
import { Data } from '../constants/charts';

function MetricLineChart(data: Data) {
  return (
    <div>
      <h3>{data.key}</h3>
      <ResponsiveContainer width="100%" aspect={3}>
        <LineChart
          data={data.values}
          margin={{top: 10, right: 10, left: 10, bottom: 10}}
        >
          <XAxis dataKey="index"/>
          <Tooltip isAnimationActive={false} labelStyle={{display: 'none'}}/>
          <CartesianGrid strokeDasharray="3 3"/>
          <Legend verticalAlign="bottom"/>
          <YAxis/>
          <Line
            type="monotone"
            dataKey="value"
            isAnimationActive={false}
            connectNulls={true}
            stroke={data.color || CHARTS_COLORS[0]}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default MetricLineChart;
