import * as React from 'react';
import { BrowserRouter, Link, Redirect, Route, Switch } from 'react-router-dom';

import './app.less';

import Footer from './footer';
import Header from './header';

import Cli from './cli';
import Deploy from './deploy';

export interface AppState {
  currentTab: string;
}

export default class App extends React.Component<{}, AppState> {
  constructor(props: any) {
    super(props);
    this.state = {
      currentTab: location.pathname === '/cli' ? '/cli' : '/deploy'
    };
  }

  public setTab = (tab: string) => {
    this.setState({currentTab: tab});
  };

  public render() {
    return (
      <BrowserRouter>
        <section id="root" className="hero is-fullheight">
          <Header/>
          <div className="hero-body layout">
            <div className="container">
              <div className="columns">
                <div className="column">
                  <div className="column">
                    <div className="tabs is-small">
                      <ul>
                        <li className={this.state.currentTab === '/cli' ? 'is-active' : ''}>
                          <Link to="/cli" onClick={() => this.setTab('/cli')}>Install CLI</Link>
                        </li>
                        <li className={this.state.currentTab === '/deploy' ? 'is-active' : ''}>
                          <Link to="/deploy" onClick={() => this.setTab('/deploy')}>Deploy</Link>
                        </li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
              <div className="columns">
                <div className="column">
                  <Switch>
                    <Route path="/cli" component={Cli}/>
                    <Route path="/deploy" component={Deploy}/>
                    <Route path="*" render={() => <Redirect to="/deploy"/>}/>
                  </Switch>
                </div>
              </div>
            </div>
          </div>
          <Footer/>
        </section>
      </BrowserRouter>
    );
  }
}
