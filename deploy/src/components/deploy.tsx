import * as React from 'react';

import * as jsYaml from 'js-yaml';

import { ConfigInterface } from '../interfaces/config';
import { VALUES } from '../libs/artifacts';

import Preview from './preview';
import Settings from './settings';

export interface DeployState {
  currentTab: string;
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
}

export default class Deploy extends React.Component<{}, DeployState> {

  constructor(props: any) {
    super(props);
    this.state = {
      config: {},
      currentTab: 'Settings',
      defaultConfig: jsYaml.safeLoad(VALUES),
    };
  }

  public updateConfig = (config: ConfigInterface) => {
    this.setState({config});
  };

  public setTab = (tab: string) => {
    this.setState({currentTab: tab});
  };

  public render() {
    return (
      <div>
        <div className="columns">
          <div className="column">
            {this.state.currentTab === 'Settings' &&
            <button
              className="button is-small is-info is-pulled-right"
              onClick={() => this.setTab('Preview')}
            >
                <span className="icon is-small">
                  <i className="fas fa-eye"/>
                </span> <span>View</span>
            </button>
            }
            {this.state.currentTab === 'Preview' &&
            <button
              className="button is-small is-info is-pulled-right"
              onClick={() => this.setTab('Settings')}
            >
              <span className="icon is-small">
                <i className="fas fa-pen"/>
              </span> <span>Edit</span>
            </button>
            }
          </div>
        </div>
        {this.state.currentTab === 'Settings' &&
        <Settings
          config={this.state.config}
          defaultConfig={this.state.defaultConfig}
          updateConfig={(config: ConfigInterface) => this.updateConfig(config)}
        />
        }
        {this.state.currentTab === 'Preview' &&
        <Preview config={this.state.config} defaultConfig={this.state.defaultConfig}/>
        }
      </div>
    );

  }
}
