import * as React from 'react';

import * as jsYaml from 'js-yaml';

import { AppState } from '../interfaces/app';
import { ConfigInterface } from '../interfaces/config';
import { VALUES } from '../libs/artifacts';
import './app.less';
import Footer from './footer';
import Header from './header';
import Preview from './preview';
import Settings from './settings';

export default class extends React.Component<{}, AppState> {

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
      <section id="root" className="hero is-fullheight">
        <Header/>
        <div className="hero-body layout">
          <div className="container">
            <div className="columns">
              <div className="column">
                <div className="tabs is-small">
                  <ul>
                    <li
                      className={this.state.currentTab === 'Settings' ? 'is-active' : ''}
                      onClick={() => this.setTab('Settings')}
                    >
                      <a>Settings</a>
                    </li>
                    <li
                      className={this.state.currentTab === 'Preview' ? 'is-active' : ''}
                      onClick={() => this.setTab('Preview')}
                    >
                      <a>Configuration File</a>
                    </li>
                  </ul>
                </div>
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
            <Preview config={this.state.config}/>
            }
          </div>
        </div>
        <Footer/>
      </section>
    );
  }
}
