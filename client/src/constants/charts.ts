export const CHARTS_COLORS = [
  '#364958',
  '#537399',
  '#A3C3D9',
  '#ae70a1',
  '#ff83d3',
  '#ffc5dd',
];

export interface DataPoint {
  [key: string]: number | boolean | string;
}

export interface Data {
  values: DataPoint[];
  key: string;
  color?: string;
}
