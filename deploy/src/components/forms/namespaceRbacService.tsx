import * as _ from 'lodash';
import * as React from 'react';

import { ConfigInterface, IngressInterface, ResourcesInterface, SERVICE_TYPES } from '../../interfaces/config';
import PreviewForm from './previewForm';
import Resources from './resources';

export interface Props {
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
  updateConfig: (config: ConfigInterface) => void;
}

interface State {
  config: ConfigInterface;
}

export default class NamespaceRbacService extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      config: this.props.config,
    };
  }

  public updateNameSpace = (value: string) => {
    const config = _.cloneDeep(this.state.config);
    config.namespace = value;
    this.setState({config});
  };

  public updateRbac = (value: boolean) => {
    const config = _.cloneDeep(this.state.config);
    config.rbac = {enabled: value};
    this.setState({config});
  };

  public updateServiceType = (value: SERVICE_TYPES) => {
    const config = _.cloneDeep(this.state.config);
    if (config.ingress && config.ingress.enabled) {
      config.serviceType = 'ClusterIP';
    } else {
      config.serviceType = value;
    }
    this.setState({config});
  };

  public updateResources = (resources: ResourcesInterface) => {
    const config = _.cloneDeep(this.state.config);
    if (_.isNil(config.ingress)) {
      config.ingress = {resources} as IngressInterface;
    } else {
      config.ingress.resources = resources;
    }
    this.setState({config});
  };

  public updateIngress = (value: boolean) => {
    const config = _.cloneDeep(this.state.config);
    if (_.isNil(config.ingress)) {
      config.ingress = {enabled: value} as IngressInterface;
    } else {
      config.ingress.enabled = value;
    }
    if (value) {
      config.serviceType = 'ClusterIP';
    } else {
      config.serviceType = 'LoadBalancer';
      delete config.ingress;
    }
    this.setState({config});
  };

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (!_.isEqual(this.state.config, prevState.config)) {
      this.props.updateConfig(this.state.config);
    }
  }

  public render() {
    const currentConfig = () => {
      const config: ConfigInterface = {};
      if (!_.isNil(this.state.config.namespace)) {
        config.namespace = this.state.config.namespace;
      }
      if (!_.isNil(this.state.config.rbac)) {
        config.rbac = this.state.config.rbac;
      }
      if (!_.isNil(this.state.config.ingress)) {
        config.ingress = this.state.config.ingress;
      }
      if (!_.isNil(this.state.config.serviceType)) {
        config.serviceType = this.state.config.serviceType;
      }
      return config;
    };

    const defaultConfig = {
      namespace: this.props.defaultConfig.namespace,
      rbac: this.props.defaultConfig.rbac,
      ingress: this.props.defaultConfig.ingress,
      serviceType: this.props.defaultConfig.serviceType
    };

    return (
      <div className="columns">
        <div className="column is-7">
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Namespace</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={this.state.config.namespace || ''}
                    onChange={(event) => this.updateNameSpace(event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">RBAC</label>
            </div>
            <div className="field-body">
              <input
                type="checkbox"
                onChange={(event) => this.updateRbac(event.target.checked)}
              />
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Ingress</label>
            </div>
            <div className="field-body">
              <input
                type="checkbox"
                onChange={(event) => this.updateIngress(event.target.checked)}
              />
            </div>
          </div>
          {this.state.config.ingress && this.state.config.ingress.enabled &&
          <Resources
            config={this.state.config.ingress.resources}
            updateConfig={this.updateResources}
            name="Ingress"
          />
          }
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Service type</label>
            </div>
            <div className="field-body">
              <div className="select">
                <select
                  onChange={(event) => this.updateServiceType(event.target.value as SERVICE_TYPES)}
                  value={this.state.config.serviceType || 'ClusterIp'}
                >
                  <option value="ClusterIp">ClusterIp</option>
                  <option value="LoadBalancer">LoadBalancer</option>
                  <option value="NodePort">NodePort</option>
                </select>
              </div>
            </div>
          </div>
        </div>
        <PreviewForm currentConfig={currentConfig()} defaultConfig={defaultConfig}/>
      </div>
    );
  }
}
