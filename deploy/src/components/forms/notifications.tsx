import * as _ from 'lodash';
import * as React from 'react';

import {
  ConfigInterface,
  IntegrationsInterface,
  IntegrationsStrInterface,
} from '../../interfaces/config';
import { checkArray, parseYaml } from '../../libs/utils';
import PreviewForm from './previewForm';

export interface Props {
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
  updateConfig: (config: ConfigInterface) => void;
}

interface State {
  config: ConfigInterface;
}

export default class Notifications extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      config: this.props.config,
    };
  }

  public update = (key: string, value: string) => {
    const config = _.cloneDeep(this.state.config);
    const valueJson = parseYaml(value);

    if (_.isNil(config.integrations)) {
      config.integrations = {} as IntegrationsInterface;
    }
    if (_.isNil(config.integrationsStr)) {
      config.integrationsStr = {} as IntegrationsStrInterface;
    }

    if (key === 'slack') {
      config.integrationsStr.slack = value;
      if (checkArray(valueJson)) {
        delete config.integrations.slack;
      } else {
        config.integrations.slack = valueJson;
      }
    } else if (key === 'hipchat') {
      config.integrationsStr.hipchat = value;
      if (checkArray(valueJson)) {
        delete config.integrations.hipchat;
      } else {
        config.integrations.hipchat = valueJson;
      }
    } else if (key === 'mattermost') {
      config.integrationsStr.mattermost = value;
      if (checkArray(valueJson)) {
        delete config.integrations.mattermost;
      } else {
        config.integrations.mattermost = valueJson;
      }
    } else if (key === 'discord') {
      config.integrationsStr.discord = value;
      if (checkArray(valueJson)) {
        delete config.integrations.discord;
      } else {
        config.integrations.discord = valueJson;
      }
    } else if (key === 'pagerduty') {
      config.integrationsStr.pagerduty = value;
      if (checkArray(valueJson)) {
        delete config.integrations.pagerduty;
      } else {
        config.integrations.pagerduty = valueJson;
      }
    } else if (key === 'webhooks') {
      config.integrationsStr.webhooks = value;
      if (checkArray(valueJson)) {
        delete config.integrations.webhooks;
      } else {
        config.integrations.webhooks = valueJson;
      }
    }
    this.setState({config});
  };

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (!_.isEqual(this.state.config, prevState.config)) {
      this.props.updateConfig(this.state.config);
    }
  }

  public render() {
    const currentIntegrationsConfig = () => {
      const config: ConfigInterface = {};
      if (!_.isNil(this.state.config.integrations)) {
        config.integrations = this.state.config.integrations;
      }
      return config;
    };

    const defaultIntegrationsConfig = {
      integrations: this.props.defaultConfig.integrations,
    };

    return (
      <div className="columns">
        <div className="column">
          <div className="columns">
            <div className="column is-7">
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Slack</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <textarea
                        className="textarea"
                        rows={2}
                        value={this.state.config.integrationsStr ?
                          this.state.config.integrationsStr.slack || '' :
                          ''}
                        onChange={(event) => this.update('slack', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Hipchat</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <textarea
                        className="textarea"
                        rows={2}
                        value={this.state.config.integrationsStr ?
                          this.state.config.integrationsStr.hipchat || '' :
                          ''}
                        onChange={(event) => this.update('hipchat', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Mattermost</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <textarea
                        className="textarea"
                        rows={2}
                        value={this.state.config.integrationsStr ?
                          this.state.config.integrationsStr.mattermost || '' :
                          ''}
                        onChange={(event) => this.update('mattermost', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Discord</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <textarea
                        className="textarea"
                        rows={2}
                        value={this.state.config.integrationsStr ?
                          this.state.config.integrationsStr.discord || '' :
                          ''}
                        onChange={(event) => this.update('discord', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Pagerduty</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <textarea
                        className="textarea"
                        rows={2}
                        value={this.state.config.integrationsStr ?
                          this.state.config.integrationsStr.pagerduty || '' :
                          ''}
                        onChange={(event) => this.update('pagerduty', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Webhooks</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <textarea
                        className="textarea"
                        rows={2}
                        value={this.state.config.integrationsStr ?
                          this.state.config.integrationsStr.webhooks || '' :
                          ''}
                        onChange={(event) => this.update('webhooks', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <PreviewForm
              currentConfig={currentIntegrationsConfig()}
              defaultConfig={defaultIntegrationsConfig}
            />
          </div>
        </div>
      </div>
    );
  }
}
