import * as React from 'react';
import { ConfigInterface } from '../interfaces/config';
import NamespaceRbacService from './forms/namespaceRbacService';

export interface Props {
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
  updateConfig: (config: ConfigInterface) => void;
}

export default class Settings extends React.Component<Props, Object> {
  public render() {
    return (
      <div className="columns">
        <div className="column is-3">
          <aside className="menu">
            <p className="menu-label">
              Deployment configuration
            </p>
            <ul className="menu-list">
              <li><a>Namespace & RBAC & Service</a></li>
              <li><a>Root user</a></li>
              <li><a>Node Scheduling</a></li>
            </ul>
            <p className="menu-label">
              Persistence
            </p>
            <ul className="menu-list">
              <li><a>Logs</a></li>
              <li><a>Repos</a></li>
              <li><a>Upload</a></li>
              <li><a>Data</a></li>
              <li><a>Outputs</a></li>
            </ul>
            <p className="menu-label">
              Single Sign On
            </p>
            <ul className="menu-list">
              <li><a>Github</a></li>
              <li><a>Gitlab</a></li>
              <li><a>Bitbucket</a></li>
              <li><a>LDAP</a></li>
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
              <li><a>Notifications</a></li>
              <li><a>Private Registries</a></li>
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
          <NamespaceRbacService
            config={this.props.config}
            defaultConfig={this.props.defaultConfig}
            updateConfig={this.props.updateConfig}
          />
        </div>
      </div>
    );
  }
}
