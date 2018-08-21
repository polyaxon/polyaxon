import * as _ from 'lodash';
import * as React from 'react';

import { AuthInterface, ConfigInterface, SSODefInterface } from '../../interfaces/config';
import PreviewForm from './previewForm';

export interface Props {
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
  updateConfig: (config: ConfigInterface) => void;
}

interface State {
  config: ConfigInterface;
}

export default class AuthGithub extends React.Component<Props, State> {
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

    if (_.isNil(config.auth.github)) {
      config.auth.github = {} as SSODefInterface;
    }

    if (value) {
      config.auth.github.enabled = value;
    } else {
      delete config.auth.github;
    }
    this.setState({config});
  };

  public update = (key: string, value: string) => {
    const config = _.cloneDeep(this.state.config);
    if (_.isNil(config.auth)) {
      config.auth = {} as AuthInterface;
    }

    if (_.isNil(config.auth.github)) {
      config.auth.github = {} as SSODefInterface;
    }

    if (key === 'clientId') {
      config.auth.github.clientId = value;
    } else if (key === 'clientSecret') {
      config.auth.github.clientSecret = value;
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
      if (!_.isNil(this.state.config.auth) && !_.isNil(this.state.config.auth.github)) {
        config.github = this.state.config.auth.github;
      }
      return config;
    };

    const defaultConfig = {
      github: this.props.defaultConfig.auth ? this.props.defaultConfig.auth.github : {},
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
                      (this.state.config.auth && this.state.config.auth.github) ?
                      this.state.config.auth.github.clientId || '' :
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
                      (this.state.config.auth && this.state.config.auth.github) ?
                      this.state.config.auth.github.clientSecret || '' :
                      ''}
                    onChange={(event) => this.update('clientSecret', event.target.value)}
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
