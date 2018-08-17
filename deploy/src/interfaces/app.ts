import { ConfigInterface } from './config';

export interface AppState {
  currentTab: string;
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
}
