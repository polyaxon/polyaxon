export interface BaseState {
  tags: Array<{ label: string, value: string }>;
  readme: string;
  description: string;
  name: string;
}

export const BaseEmptyState = {
  tags: [],
  readme: '',
  description: '',
  name: '',
};
