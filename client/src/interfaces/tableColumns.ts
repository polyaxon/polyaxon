export interface ColumnInterface {
  name?: string;
  field: string;
  type: 'value' | 'datetime' | 'scalar' | 'bool';
  desc: string;
  sort: boolean;
  icon: string;
  dataIndex?: string;
  render?: any;
  width?: number;
  fixed?: boolean;
}
