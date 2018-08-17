import { ConfigInterface } from './config';

export interface AppState {
  currentTab: 'settings' | 'preview';
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
}
