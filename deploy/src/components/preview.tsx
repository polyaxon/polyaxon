import * as jsYaml from 'js-yaml';
import * as _ from 'lodash';
import * as React from 'react';

import { ConfigInterface } from '../interfaces/config';

export interface Props {
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
}

export interface State {
  dataRadio: string;
}

export default class Preview extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      dataRadio: 'yaml',
    };
  }

  public updateRenderer = (value: string) => {
    this.setState({dataRadio: value});
  };

  public render() {
    const renderConfig = () => {
      const config: ConfigInterface = {};
      if (!_.isNil(this.props.config.namespace)) {
        config.namespace = this.props.config.namespace;
      }
      if (!_.isNil(this.props.config.rbac)) {
        config.rbac = this.props.config.rbac;
      }
      if (!_.isNil(this.props.config.ingress)) {
        config.ingress = this.props.config.ingress;
      }
      if (!_.isNil(this.props.config.serviceType)) {
        config.serviceType = this.props.config.serviceType;
      }
      if (!_.isNil(this.props.config.user)) {
        config.user = this.props.config.user;
      }
      if (!_.isNil(this.props.config.timeZone)) {
        config.passwordLength = this.props.config.passwordLength;
      }
      if (!_.isNil(this.props.config.timeZone)) {
        config.timeZone = this.props.config.timeZone;
      }
      if (!_.isNil(this.props.config.nodeSelectors)) {
        config.nodeSelectors = this.props.config.nodeSelectors;
      }
      if (!_.isNil(this.props.config.affinity)) {
        config.affinity = this.props.config.affinity;
      }
      if (!_.isNil(this.props.config.tolerations)) {
        config.tolerations = this.props.config.tolerations;
      }
      if (!_.isNil(this.props.config.limitResources)) {
        config.limitResources = this.props.config.limitResources;
      }
      if (!_.isNil(this.props.config.api)) {
        config.api = this.props.config.api;
      }
      if (!_.isNil(this.props.config.scheduler)) {
        config.scheduler = this.props.config.scheduler;
      }
      if (!_.isNil(this.props.config.hpsearch)) {
        config.hpsearch = this.props.config.hpsearch;
      }
      if (!_.isNil(this.props.config.eventsHandlers)) {
        config.eventsHandlers = this.props.config.eventsHandlers;
      }
      if (!_.isNil(this.props.config.eventMonitors)) {
        config.eventMonitors = this.props.config.eventMonitors;
      }
      if (!_.isNil(this.props.config.postgresql)) {
        config.postgresql = this.props.config.postgresql;
      }
      if (!_.isNil(this.props.config.persistence)) {
        config.persistence = this.props.config.persistence;
      }
      if (!_.isNil(this.props.config.auth)) {
        config.auth = this.props.config.auth;
      }
      if (!_.isNil(this.props.config.email)) {
        config.email = this.props.config.email;
      }
      if (!_.isNil(this.props.config.integrations)) {
        config.integrations = this.props.config.integrations;
      }
      if (!_.isNil(this.props.config.privateRegistries)) {
        config.privateRegistries = this.props.config.privateRegistries;
      }

      if (this.state.dataRadio === 'json') {
        return JSON.stringify(config, null, 4);
      } else {
        return jsYaml.dump(config);
      }
    };

    return (
      <div className="columns preview">
        <div className="column is-8 is-offset-2">
          <div className="columns">
            <div className="column">
              <div className="field is-horizontal">
                <label className="radio">
                  <input
                    type="radio"
                    value="yaml"
                    checked={this.state.dataRadio === 'yaml'}
                    onChange={(event) => this.updateRenderer('yaml')}
                  /> To Yaml
                </label>
                <label className="radio">
                  <input
                    type="radio"
                    value="json"
                    checked={this.state.dataRadio === 'json'}
                    onChange={(event) => this.updateRenderer('json')}
                  /> To Json
                </label>
              </div>

            </div>
          </div>
          <div className="columns">
            <div className="column">
              <div className="content">
                <hr className="navbar-divider"/>
                <h6>config.yml</h6>
              </div>
              <figure className="content-figure">
                <pre className="content content-output content-preview">
                  <p>
                    {renderConfig()}
                  </p>
                </pre>
              </figure>
            </div>
          </div>
          <div className="columns">
            <div className="column">
              <div className="content">
                <hr className="navbar-divider"/>
                <h6>Commands</h6>
              </div>
              <figure className="content-figure">
                <pre className="content content-output code">
                  <code>
                    <span className="bash">
                      helm repo add polyaxon https://charts.polyaxon.com
                    </span>
                    <span className="bash">
                      helm repo update
                    </span>
                    <span className="bash">
                      kubectl create namespace {this.props.config.namespace || this.props.defaultConfig.namespace}
                    </span>
                    <span className="bash">
                      helm install polyaxon/polyaxon --name=polyaxon --namespace={this.props.config.namespace || this.props.defaultConfig.namespace} -f config.yml
                    </span>
                  </code>
                </pre>
              </figure>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
