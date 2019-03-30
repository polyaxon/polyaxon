export interface BaseState {
  project: string;
  tags: Array<{ label: string, value: string }>;
  readme: string;
  description: string;
  name: string;
}

export const BaseEmptyState = {
  project: '',
  tags: [],
  readme: '',
  description: '',
  name: '',
};
