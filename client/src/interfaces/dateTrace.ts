import { TraceModes, TraceTypes } from '../models/chart';

export interface DataTrace {
  x: Plotly.Datum[];
  y: Plotly.Datum[];
  z?: Plotly.Datum[];
}

export interface Trace extends DataTrace {
  name: string;
  mode: TraceModes;
  type: TraceTypes;
  line?: Partial<Plotly.ScatterLine>;
  marker?: Partial<Plotly.PlotMarker>;
}
