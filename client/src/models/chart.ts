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
  | 'histogram'
  | 'parallel';

export class ChartModel {
  public name: string;
  public metricNames: string[];
  public paramNames: string[];
  public experiments: string[];
  public type: ChartTypes;
}
