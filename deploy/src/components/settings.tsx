import * as React from 'react';
import { ConfigInterface } from '../interfaces/config';
import NamespaceRbacService from './forms/namespaceRbacService';
import NodeScheduling from './forms/nodeScheduling';
import PersistenceData from './forms/persistenceData';
import PersistenceOutputs from './forms/persistenceOutputs';
import PersistenceLogs from './forms/persistenceLogs';
import PersistenceRepos from './forms/persistenceRepos';
import PersistenceUpload from './forms/persistenceUpload';
import RootUser from './forms/rootUser';
import AuthGithub from './forms/authGithub';
import AuthGitlab from './forms/authGitlab';
import AuthBitbucket from './forms/authBitbucket';
import AuthAzure from './forms/authAzure';
import AuthLDAP from './forms/authLDAP';
import ReplicationResources from './forms/replicationResources';
import Email from './forms/email';
import Notifications from './forms/notifications';
import Registries from './forms/registries';
import Postgres from './forms/postgres';

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
        <div className="column is-2">
          <aside className="menu">
            <p className="menu-label">
              General config
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
              <li
                className={this.state.currentTab === 'ReplicationResources' ? 'is-active' : ''}
                onClick={() => this.setTab('ReplicationResources')}
              >
                <a>Replication & Resources</a>
              </li>
              <li
                className={this.state.currentTab === 'Postgres' ? 'is-active' : ''}
                onClick={() => this.setTab('Postgres')}
              >
                <a>Postgres HA</a>
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
                className={this.state.currentTab === 'PersistenceOutputs' ? 'is-active' : ''}
                onClick={() => this.setTab('PersistenceOutputs')}
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
                className={this.state.currentTab === 'SSOAzure' ? 'is-active' : ''}
                onClick={() => this.setTab('SSOAzure')}
              >
                <a>Azure</a>
              </li>
              <li
                className={this.state.currentTab === 'SSOLDAP' ? 'is-active' : ''}
                onClick={() => this.setTab('SSOLDAP')}
              >
                <a>LDAP</a>
              </li>
            </ul>
            <p className="menu-label">
              Integrations
            </p>
            <ul className="menu-list">
              <li
                className={this.state.currentTab === 'Email' ? 'is-active' : ''}
                onClick={() => this.setTab('Email')}
              >
                <a>Email</a>
              </li>
              <li
                className={this.state.currentTab === 'Notifications' ? 'is-active' : ''}
                onClick={() => this.setTab('Notifications')}
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
          </aside>
        </div>
        <div className="column is-10">
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
          {this.state.currentTab === 'NodeScheduling' &&
          <NodeScheduling
            config={this.props.config}
            defaultConfig={this.props.defaultConfig}
            updateConfig={this.props.updateConfig}
          />
          }
          {this.state.currentTab === 'ReplicationResources' &&
          <ReplicationResources
            config={this.props.config}
            defaultConfig={this.props.defaultConfig}
            updateConfig={this.props.updateConfig}
          />
          }
          {this.state.currentTab === 'Postgres' &&
          <Postgres
            config={this.props.config}
            defaultConfig={this.props.defaultConfig}
            updateConfig={this.props.updateConfig}
          />
          }
          {this.state.currentTab === 'PersistenceLogs' &&
          <PersistenceLogs
            config={this.props.config}
            defaultConfig={this.props.defaultConfig}
            updateConfig={this.props.updateConfig}
          />
          }
          {this.state.currentTab === 'PersistenceRepos' &&
          <PersistenceRepos
            config={this.props.config}
            defaultConfig={this.props.defaultConfig}
            updateConfig={this.props.updateConfig}
          />
          }
          {this.state.currentTab === 'PersistenceUpload' &&
          <PersistenceUpload
            config={this.props.config}
            defaultConfig={this.props.defaultConfig}
            updateConfig={this.props.updateConfig}
          />
          }
          {this.state.currentTab === 'PersistenceData' &&
          <PersistenceData
            config={this.props.config}
            defaultConfig={this.props.defaultConfig}
            updateConfig={this.props.updateConfig}
          />
          }
          {this.state.currentTab === 'PersistenceOutputs' &&
          <PersistenceOutputs
            config={this.props.config}
            defaultConfig={this.props.defaultConfig}
            updateConfig={this.props.updateConfig}
          />
          }
          {this.state.currentTab === 'SSOGithub' &&
          <AuthGithub
            config={this.props.config}
            defaultConfig={this.props.defaultConfig}
            updateConfig={this.props.updateConfig}
          />
          }
          {this.state.currentTab === 'SSOGitlab' &&
          <AuthGitlab
            config={this.props.config}
            defaultConfig={this.props.defaultConfig}
            updateConfig={this.props.updateConfig}
          />
          }
          {this.state.currentTab === 'SSOBitbucket' &&
          <AuthBitbucket
            config={this.props.config}
            defaultConfig={this.props.defaultConfig}
            updateConfig={this.props.updateConfig}
          />
          }
          {this.state.currentTab === 'SSOAzure' &&
          <AuthAzure
            config={this.props.config}
            defaultConfig={this.props.defaultConfig}
            updateConfig={this.props.updateConfig}
          />
          }
          {this.state.currentTab === 'SSOLDAP' &&
          <AuthLDAP
            config={this.props.config}
            defaultConfig={this.props.defaultConfig}
            updateConfig={this.props.updateConfig}
          />
          }
          {this.state.currentTab === 'Email' &&
          <Email
            config={this.props.config}
            defaultConfig={this.props.defaultConfig}
            updateConfig={this.props.updateConfig}
          />
          }
          {this.state.currentTab === 'Notifications' &&
          <Notifications
            config={this.props.config}
            defaultConfig={this.props.defaultConfig}
            updateConfig={this.props.updateConfig}
          />
          }
          {this.state.currentTab === 'PrivateRegistries' &&
          <Registries
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
