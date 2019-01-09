import * as _ from 'lodash';
import * as React from 'react';

import { AuthInterface, ConfigInterface, GitlabInterface } from '../../interfaces/config';
import PreviewForm from './previewForm';

export interface Props {
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
  updateConfig: (config: ConfigInterface) => void;
}

interface State {
  config: ConfigInterface;
}

export default class AuthGitlab extends React.Component<Props, State> {
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

    if (_.isNil(config.auth.gitlab)) {
      config.auth.gitlab = {} as GitlabInterface;
    }

    if (value) {
      config.auth.gitlab.enabled = value;
    } else {
      delete config.auth.gitlab;
    }
    this.setState({config});
  };

  public update = (key: string, value: string) => {
    const config = _.cloneDeep(this.state.config);
    if (_.isNil(config.auth)) {
      config.auth = {} as AuthInterface;
    }

    if (_.isNil(config.auth.gitlab)) {
      config.auth.gitlab = {} as GitlabInterface;
    }

    if (key === 'clientId') {
      config.auth.gitlab.clientId = value;
    } else if (key === 'clientSecret') {
      config.auth.gitlab.clientSecret = value;
    } else if (key === 'url') {
      config.auth.gitlab.url = value;
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
      if (!_.isNil(this.state.config.auth) && !_.isNil(this.state.config.auth.gitlab)) {
        config.gitlab = this.state.config.auth.gitlab;
      }
      return config;
    };

    const defaultConfig = {
      gitlab: this.props.defaultConfig.auth ? this.props.defaultConfig.auth.gitlab : {},
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
                      (this.state.config.auth && this.state.config.auth.gitlab) ?
                      this.state.config.auth.gitlab.clientId || '' :
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
                      (this.state.config.auth && this.state.config.auth.gitlab) ?
                      this.state.config.auth.gitlab.clientSecret || '' :
                      ''}
                    onChange={(event) => this.update('clientSecret', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Url</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={
                      (this.state.config.auth && this.state.config.auth.gitlab) ?
                      this.state.config.auth.gitlab.url || '' :
                      ''}
                    onChange={(event) => this.update('url', event.target.value)}
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
