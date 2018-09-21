export type TraceModes =
  'lines'
  | 'markers'
  | 'text'
  | 'lines+markers'
  | 'text+markers'
  | 'text+lines'
  | 'text+lines+markers'
  | 'none';

export type TraceTypes =
  'bar'
  | 'histogram'
  | 'pointcloud'
  | 'scatter'
  | 'scattergl'
  | 'scatter3d'
  | 'surface';

export type ChartTypes =
  'bar'
  | 'line'
  | 'scatter'
  | 'parallel';

export class ChartModel {
  public name: string;
  public metricNames: string[];
  public type: ChartTypes;
}
