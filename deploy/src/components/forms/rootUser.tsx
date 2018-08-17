import * as _ from 'lodash';
import * as React from 'react';

import { ConfigInterface, UserInterface } from '../../interfaces/config';
import PreviewForm from './previewForm';

export interface Props {
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
  updateConfig: (config: ConfigInterface) => void;
}

interface State {
  config: ConfigInterface;
}

export default class RootUser extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      config: this.props.config,
    };
  }

  public updateUser = (key: string, value: string) => {
    const config = _.cloneDeep(this.state.config);
    if (_.isNil(config.user)) {
      config.user = {} as UserInterface;
    }
    if (key === 'username') {
      config.user.username = value;
    } else if (key === 'email') {
      config.user.email = value;
    } else if (key === 'password') {
      config.user.password = value;
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
      if (!_.isNil(this.state.config.user)) {
        config.user = this.state.config.user;
      }
      return config;
    };

    const defaultConfig = {
      user: this.props.defaultConfig.user,
    };

    return (
      <div className="columns">
        <div className="column is-7">
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Username</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={this.state.config.user ? this.state.config.user.username || '' : ''}
                    onChange={(event) => this.updateUser('username', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Email</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={this.state.config.user ? this.state.config.user.email || '' : ''}
                    onChange={(event) => this.updateUser('email', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Password</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={this.state.config.user ? this.state.config.user.password || '' : ''}
                    onChange={(event) => this.updateUser('password', event.target.value)}
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
