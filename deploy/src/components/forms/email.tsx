import * as _ from 'lodash';
import * as React from 'react';

import { ConfigInterface, EmailInterface } from '../../interfaces/config';
import PreviewForm from './previewForm';

export interface Props {
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
  updateConfig: (config: ConfigInterface) => void;
}

interface State {
  config: ConfigInterface;
}

export default class Email extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      config: this.props.config,
    };
  }

  public update = (key: string, value: string) => {
    const config = _.cloneDeep(this.state.config);
    if (_.isNil(config.email)) {
      config.email = {} as EmailInterface;
    }
    if (key === 'host') {
      config.email.host = value;
    } else if (key === 'hostUser') {
      config.email.hostUser = value;
    } else if (key === 'port') {
      const valueInt = parseInt(value, 10);
      if (isNaN(valueInt)) {
        delete config.email.port;
      } else {
        config.email.port = valueInt;
      }
    } else if (key === 'hostPassword') {
      config.email.hostPassword = value;
    }
    this.setState({config});
  };

  public updateTls = (value: boolean) => {
    const config = _.cloneDeep(this.state.config);
    if (_.isNil(config.email)) {
      config.email = {} as EmailInterface;
    }
    config.email.useTls = value;
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
      if (!_.isNil(this.state.config.email)) {
        config.email = this.state.config.email;
      }
      return config;
    };

    const defaultConfig = {
      email: this.props.defaultConfig.email,
    };

    return (
      <div className="columns">
        <div className="column is-7">
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Host</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={this.state.config.email ? this.state.config.email.host || '' : ''}
                    onChange={(event) => this.update('host', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Port</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={this.state.config.email ? this.state.config.email.port || '' : ''}
                    onChange={(event) => this.update('port', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Hot User</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={this.state.config.email ? this.state.config.email.hostUser || '' : ''}
                    onChange={(event) => this.update('hostUser', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Host Password</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={this.state.config.email ? this.state.config.email.hostPassword || '' : ''}
                    onChange={(event) => this.update('hostPassword', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Use Tls</label>
            </div>
            <div className="field-body">
              <input
                type="checkbox"
                onChange={(event) => this.updateTls(event.target.checked)}
              />
            </div>
          </div>
        </div>
        <PreviewForm currentConfig={currentConfig()} defaultConfig={defaultConfig}/>
      </div>
    );
  }
}
