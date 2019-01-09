import * as _ from 'lodash';
import * as React from 'react';

import { AuthInterface, ConfigInterface, AzureInterface } from '../../interfaces/config';
import PreviewForm from './previewForm';

export interface Props {
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
  updateConfig: (config: ConfigInterface) => void;
}

interface State {
  config: ConfigInterface;
}

export default class AuthAzure extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      config: this.props.config,
    };
  }

  public updateEnabled = (value: boolean) => {
    const config = _.cloneDeep(this.state.config);
    if (_.isNil(config.auth)) {
      config.auth = {} as AuthInterface;
    }

    if (_.isNil(config.auth.azure)) {
      config.auth.azure = {} as AzureInterface;
    }

    if (value) {
      config.auth.azure.enabled = value;
    } else {
      delete config.auth.azure;
    }
    this.setState({config});
  };

  public update = (key: string, value: string) => {
    const config = _.cloneDeep(this.state.config);
    if (_.isNil(config.auth)) {
      config.auth = {} as AuthInterface;
    }

    if (_.isNil(config.auth.azure)) {
      config.auth.azure = {} as AzureInterface;
    }

    if (key === 'clientId') {
      config.auth.azure.clientId = value;
    } else if (key === 'clientSecret') {
      config.auth.azure.clientSecret = value;
    } else if (key === 'tenantId') {
      config.auth.azure.tenantId = value;
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
      const config: AuthInterface = {};
      if (!_.isNil(this.state.config.auth) && !_.isNil(this.state.config.auth.azure)) {
        config.azure = this.state.config.auth.azure;
      }
      return config;
    };

    const defaultConfig = {
      azure: this.props.defaultConfig.auth ? this.props.defaultConfig.auth.azure : {},
    };

    return (
      <div className="columns">
        <div className="column is-7">
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Enable</label>
            </div>
            <div className="field-body">
              <input
                type="checkbox"
                onChange={(event) => this.updateEnabled(event.target.checked)}
              />
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">clientId</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={
                      (this.state.config.auth && this.state.config.auth.azure) ?
                      this.state.config.auth.azure.clientId || '' :
                      ''}
                    onChange={(event) => this.update('clientId', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">clientSecret</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={
                      (this.state.config.auth && this.state.config.auth.azure) ?
                      this.state.config.auth.azure.clientSecret || '' :
                      ''}
                    onChange={(event) => this.update('clientSecret', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">tenantId</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={
                      (this.state.config.auth && this.state.config.auth.azure) ?
                      this.state.config.auth.azure.tenantId || '' :
                      ''}
                    onChange={(event) => this.update('tenantId', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        <PreviewForm currentConfig={currentConfig()} defaultConfig={defaultConfig}/>
      </div>
    );
  }
}
