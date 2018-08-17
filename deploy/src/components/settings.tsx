import * as React from 'react';
import { ConfigInterface } from '../interfaces/config';
import NamespaceRbacService from './forms/namespaceRbacService';
import RootUser from './forms/rootUser';

export interface State {
  currentTab: string;
}

export interface Props {
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
  updateConfig: (config: ConfigInterface) => void;
}

export default class Settings extends React.Component<Props, State> {
  constructor(props: any) {
    super(props);
    this.state = {
      currentTab: 'NamespaceRbacService',
    };
  }

  public setTab = (tab: string) => {
    this.setState({currentTab: tab});
  };

  public render() {
    return (
      <div className="columns">
        <div className="column is-3">
          <aside className="menu">
            <p className="menu-label">
              Deployment configuration
            </p>
            <ul className="menu-list">
              <li
                className={this.state.currentTab === 'NamespaceRbacService' ? 'is-active' : ''}
                onClick={() => this.setTab('NamespaceRbacService')}
              >
                <a>Namespace & RBAC & Service</a>
              </li>
              <li
                className={this.state.currentTab === 'RootUser' ? 'is-active' : ''}
                onClick={() => this.setTab('RootUser')}
              >
                <a>Root user</a>
              </li>
              <li
                className={this.state.currentTab === 'NodeScheduling' ? 'is-active' : ''}
                onClick={() => this.setTab('NodeScheduling')}
              >
                <a>Node Scheduling</a>
              </li>
            </ul>
            <p className="menu-label">
              Persistence
            </p>
            <ul className="menu-list">
              <li
                className={this.state.currentTab === 'PersistenceLogs' ? 'is-active' : ''}
                onClick={() => this.setTab('PersistenceLogs')}
              >
                <a>Logs</a>
              </li>
              <li
                className={this.state.currentTab === 'PersistenceRepos' ? 'is-active' : ''}
                onClick={() => this.setTab('PersistenceRepos')}
              >
                <a>Repos</a>
              </li>
              <li
                className={this.state.currentTab === 'PersistenceUpload' ? 'is-active' : ''}
                onClick={() => this.setTab('PersistenceUpload')}
              ><a>Upload</a>
              </li>
              <li
                className={this.state.currentTab === 'PersistenceData' ? 'is-active' : ''}
                onClick={() => this.setTab('PersistenceData')}
              ><a>Data</a>
              </li>
              <li
                className={this.state.currentTab === 'PersistenceData' ? 'is-active' : ''}
                onClick={() => this.setTab('PersistenceData')}
              ><a>Outputs</a>
              </li>
            </ul>
            <p className="menu-label">
              Single Sign On
            </p>
            <ul className="menu-list">
              <li
                className={this.state.currentTab === 'SSOGithub' ? 'is-active' : ''}
                onClick={() => this.setTab('SSOGithub')}
              >
                <a>Github</a>
              </li>
              <li
                className={this.state.currentTab === 'SSOGitlab' ? 'is-active' : ''}
                onClick={() => this.setTab('SSOGitlab')}
              >
                <a>Gitlab</a>
              </li>
              <li
                className={this.state.currentTab === 'SSOBitbucket' ? 'is-active' : ''}
                onClick={() => this.setTab('SSOBitbucket')}
              >
                <a>Bitbucket</a>
              </li>
              <li
                className={this.state.currentTab === 'SSOLDAP' ? 'is-active' : ''}
                onClick={() => this.setTab('SSOLDAP')}
              >
                <a>LDAP</a>
              </li>
            </ul>
            <p className="menu-label">
              Services Replication & Resources
            </p>
            <ul className="menu-list">
              <li><a>Api</a></li>
              <li><a>Workers</a></li>
            </ul>
            <p className="menu-label">
              Integrations
            </p>
            <ul className="menu-list">
              <li
                className={this.state.currentTab === 'Integrations' ? 'is-active' : ''}
                onClick={() => this.setTab('Integrations')}
              >
                <a>Notifications</a>
              </li>
              <li
                className={this.state.currentTab === 'PrivateRegistries' ? 'is-active' : ''}
                onClick={() => this.setTab('PrivateRegistries')}
              >
                <a>Private Registries</a>
              </li>
            </ul>
            <p className="menu-label">
              Components
            </p>
            <ul className="menu-list">
              <li><a>Postgres</a></li>
              <li><a>Redis</a></li>
              <li><a>Registry</a></li>
            </ul>
          </aside>
        </div>
        <div className="column is-9">
          {this.state.currentTab === 'NamespaceRbacService' &&
          <NamespaceRbacService
            config={this.props.config}
            defaultConfig={this.props.defaultConfig}
            updateConfig={this.props.updateConfig}
          />
          }
          {this.state.currentTab === 'RootUser' &&
          <RootUser
            config={this.props.config}
            defaultConfig={this.props.defaultConfig}
            updateConfig={this.props.updateConfig}
          />
          }
        </div>
      </div>
    );
  }
}
