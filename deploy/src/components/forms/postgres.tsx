import * as _ from 'lodash';
import * as React from 'react';

import { ConfigInterface, PostgresInterface } from '../../interfaces/config';
import PreviewForm from './previewForm';

export interface Props {
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
  updateConfig: (config: ConfigInterface) => void;
}

interface State {
  config: ConfigInterface;
  dataRadio?: string;
}

export default class Postgres extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      config: this.props.config,
      dataRadio: this.props.config.postgresql &&
      !_.isNil(this.props.config.postgresql.enabled) &&
      this.props.config.postgresql.enabled ?
        'persistence' :
        'external'
    };
  }

  public useExternal = () => {
    const config = _.cloneDeep(this.state.config);
    config.postgresql = {enabled: false} as PostgresInterface;
    if (!_.isNil(config.postgresql) && !_.isNil(config.postgresql.persistence)) {
      delete config.postgresql.persistence;
    }

    this.setState({config, dataRadio: 'external'});
  };

  public updateExternal = (key: string, value: string) => {
    const config = _.cloneDeep(this.state.config);
    if (_.isNil(config.postgresql)) {
      config.postgresql = {enabled: false} as PostgresInterface;
    }

    if (key === 'postgresUser') {
      config.postgresql.postgresUser = value;
    } else if (key === 'postgresPassword') {
      config.postgresql.postgresPassword = value;
    } else if (key === 'postgresDatabase') {
      config.postgresql.postgresDatabase = value;
    } else if (key === 'externalPostgresHost') {
      config.postgresql.externalPostgresHost = value;
    }
    this.setState({config});
  };

  public usePersistence = () => {
    const config = _.cloneDeep(this.state.config);
    config.postgresql = {persistence: {enabled: true}} as PostgresInterface;
    this.setState({config, dataRadio: 'persistence'});
  };

  public updatePersistence = (key: string, value: string) => {
    const config = _.cloneDeep(this.state.config);
    if (_.isNil(config.postgresql)) {
      config.postgresql = {persistence: {enabled: true}} as PostgresInterface;
    }

    if (key === 'size') {
      config.postgresql.persistence.size = value;
      delete config.postgresql.persistence.existingClaim;
    } else if (key === 'existingClaim') {
      config.postgresql.persistence.existingClaim = value;
      delete config.postgresql.persistence.size;
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
      if (!_.isNil(this.state.config.postgresql)) {
        config.postgresql = this.state.config.postgresql;
      }
      return config;
    };

    const defaultConfig = {
      postgresql: this.props.defaultConfig.postgresql,
    };

    return (
      <div className="columns">
        <div className="column is-7">
          <div className="field is-horizontal">
            <label className="radio">
              <input
                type="radio"
                value="persistence"
                checked={this.state.dataRadio === 'persistence'}
                onChange={(event) => this.usePersistence()}
              /> Use persistence
            </label>
            <label className="radio">
              <input
                type="radio"
                value="external"
                checked={this.state.dataRadio === 'external'}
                onChange={(event) => this.useExternal()}
              /> Use external
            </label>
          </div>

          {this.state.dataRadio === 'persistence' &&
          <div>
            <div className="field is-horizontal">
              <div className="field-label is-normal">
                <label className="label">Size</label>
              </div>
              <div className="field-body">
                <div className="field">
                  <div className="control">
                    <input
                      className="input"
                      type="text"
                      value={this.state.config.postgresql ?
                        this.state.config.postgresql.persistence.size || '' :
                        ''}
                      onChange={(event) => this.updatePersistence('size', event.target.value)}
                    />
                  </div>
                </div>
              </div>
            </div>
            <div className="field is-horizontal">
              <div className="field-label is-normal">
                <label className="label">Existing Claim</label>
              </div>
              <div className="field-body">
                <div className="field">
                  <div className="control">
                    <input
                      className="input"
                      type="text"
                      value={this.state.config.postgresql ?
                        this.state.config.postgresql.persistence.existingClaim || '' :
                        ''}
                      onChange={(event) => this.updatePersistence('existingClaim', event.target.value)}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
          }
          {this.state.dataRadio === 'external' &&
          <div>
            <div className="field is-horizontal">
              <div className="field-label is-normal">
                <label className="label">Postgres User</label>
              </div>
              <div className="field-body">
                <div className="field">
                  <div className="control">
                    <input
                      className="input"
                      type="text"
                      value={this.state.config.postgresql ?
                        this.state.config.postgresql.postgresUser || '' :
                        ''}
                      onChange={(event) => this.updateExternal('postgresUser', event.target.value)}
                    />
                  </div>
                </div>
              </div>
            </div>
            <div className="field is-horizontal">
              <div className="field-label is-normal">
                <label className="label">Postgres Password</label>
              </div>
              <div className="field-body">
                <div className="field">
                  <div className="control">
                    <input
                      className="input"
                      type="text"
                      value={this.state.config.postgresql ?
                        this.state.config.postgresql.postgresPassword || '' :
                        ''}
                      onChange={(event) => this.updateExternal('postgresPassword', event.target.value)}
                    />
                  </div>
                </div>
              </div>
            </div>
            <div className="field is-horizontal">
              <div className="field-label is-normal">
                <label className="label">Postgres name</label>
              </div>
              <div className="field-body">
                <div className="field">
                  <div className="control">
                    <input
                      className="input"
                      type="text"
                      value={this.state.config.postgresql ?
                        this.state.config.postgresql.postgresDatabase || '' :
                        ''}
                      onChange={(event) => this.updateExternal('postgresDatabase', event.target.value)}
                    />
                  </div>
                </div>
              </div>
            </div>
            <div className="field is-horizontal">
              <div className="field-label is-normal">
                <label className="label">External PostgresHost</label>
              </div>
              <div className="field-body">
                <div className="field">
                  <div className="control">
                    <input
                      className="input"
                      type="text"
                      value={this.state.config.postgresql ?
                        this.state.config.postgresql.externalPostgresHost || '' :
                        ''}
                      onChange={(event) => this.updateExternal('externalPostgresHost', event.target.value)}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
          }
        </div>
        <PreviewForm currentConfig={currentConfig()} defaultConfig={defaultConfig}/>
      </div>
    );
  }
}
