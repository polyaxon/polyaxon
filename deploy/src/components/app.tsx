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

export default class extends React.Component<Object, AppState> {

  constructor(props: any) {
    super(props);
    this.state = {
      config: {},
      currentTab: 'settings',
      defaultConfig: jsYaml.safeLoad(VALUES),
    };
  }

  public updateConfig = (config: ConfigInterface) => {
    this.setState({config});
  };

  public setTab = (tab: 'settings' | 'preview') => {
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
                      className={this.state.currentTab === 'settings' ? 'is-active' : ''}
                      onClick={() => this.setTab('settings')}
                    >
                      <a>Settings</a>
                    </li>
                    <li
                      className={this.state.currentTab === 'preview' ? 'is-active' : ''}
                      onClick={() => this.setTab('preview')}
                    >
                      <a>Configuration File</a>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
            {this.state.currentTab === 'settings' &&
            <Settings
              config={this.state.config}
              defaultConfig={this.state.defaultConfig}
              updateConfig={(config: ConfigInterface) => this.updateConfig(config)}
            />
            }
            {this.state.currentTab === 'preview' &&
            <Preview config={this.state.config}/>
            }
          </div>
        </div>
        <Footer/>
      </section>
    );
  }
}
