export interface ActionInterface {
  onDelete: () => any;
  onStop?: () => any;
  last_status?: string;
}
