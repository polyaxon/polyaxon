import { TraceModes, TraceTypes } from '../models/chart';

export interface DataTrace {
  x: Plotly.Datum[];
  y: Plotly.Datum[];
  z?: Plotly.Datum[];
}

export interface Trace extends DataTrace {
  name?: string;
  mode: TraceModes;
  type: TraceTypes;
  line?: Partial<Plotly.ScatterLine>;
  marker?: Partial<Plotly.PlotMarker>;
  connectgaps?: boolean;
  hoverinfo?: string;
  showlegend?: boolean;
  opacity?: number;
}

export interface DataDimension {
  range: number[];
  constraintrange: number[];
  label: string;
  values: number[] | string[];
  tickvals: number[];
  ticktext: string[];
}
