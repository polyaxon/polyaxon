export type ChartModes =
  'lines'
  | 'markers'
  | 'text'
  | 'lines+markers'
  | 'text+markers'
  | 'text+lines'
  | 'text+lines+markers'
  | 'none';

export class ChartModel {
  public id: number;
  public created_at: string;
  public updated_at: string;
  public name: string;
  public metricNames: string[];
  public mode: ChartModes;
}
