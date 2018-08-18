import * as _ from 'lodash';
import * as React from 'react';

import { ConfigInterface, ServiceInterface } from '../../interfaces/config';
import PreviewForm from './previewForm';

export interface Props {
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
  updateConfig: (config: ConfigInterface) => void;
}

interface State {
  config: ConfigInterface;
}

export default class ReplicationResources extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      config: this.props.config,
    };
  }

  public updateResources = (value: boolean) => {
    const config = _.cloneDeep(this.state.config);
    config.limitResources = value;
    this.setState({config});
  };

  public update = (key: string, valueStr: string) => {
    const value = parseInt(valueStr, 10);
    const config = _.cloneDeep(this.state.config);

    if (key === 'api') {
      if (_.isNil(config.api)) {
        config.api = {} as ServiceInterface;
      }
      config.api.replicas = value;
    } else if (key === 'scheduler') {
      if (_.isNil(config.scheduler)) {
        config.scheduler = {} as ServiceInterface;
      }
      config.scheduler.replicas = value;
    } else if (key === 'hpsearch') {
      if (_.isNil(config.hpsearch)) {
        config.hpsearch = {} as ServiceInterface;
      }
      config.hpsearch.replicas = value;
    } else if (key === 'eventsHandlers') {
      if (_.isNil(config.eventsHandlers)) {
        config.eventsHandlers = {} as ServiceInterface;
      }
      config.eventsHandlers.replicas = value;
    } else if (key === 'eventMonitors') {
      if (_.isNil(config.eventMonitors)) {
        config.eventMonitors = {} as ServiceInterface;
      }
      config.eventMonitors.replicas = value;
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
      if (!_.isNil(this.state.config.limitResources)) {
        config.limitResources = this.state.config.limitResources;
      }
      if (!_.isNil(this.state.config.api)) {
        config.api = this.state.config.api;
      }
      if (!_.isNil(this.state.config.scheduler)) {
        config.scheduler = this.state.config.scheduler;
      }
      if (!_.isNil(this.state.config.hpsearch)) {
        config.hpsearch = this.state.config.hpsearch;
      }
      if (!_.isNil(this.state.config.eventsHandlers)) {
        config.eventsHandlers = this.state.config.eventsHandlers;
      }
      if (!_.isNil(this.state.config.eventMonitors)) {
        config.eventMonitors = this.state.config.eventMonitors;
      }
      return config;
    };

    const defaultConfig = {
      limitResources: this.props.defaultConfig.limitResources,
      api: this.props.defaultConfig.api,
      scheduler: this.props.defaultConfig.scheduler,
      hpsearch: this.props.defaultConfig.hpsearch,
      eventsHandlers: this.props.defaultConfig.eventsHandlers,
      eventMonitors: this.props.defaultConfig.eventMonitors,
    };

    return (
      <div className="columns">
        <div className="column is-7">
          <div className="content">
            <hr className="navbar-divider"/>
            <h6>Limit Resources</h6>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Enable</label>
            </div>
            <div className="field-body">
              <input
                type="checkbox"
                onChange={(event) => this.updateResources(event.target.checked)}
              />
            </div>
          </div>
          <div className="content">
            <hr className="navbar-divider"/>
            <h6>Service Replication</h6>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Api</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="number"
                    min="1"
                    value={this.state.config.api ? this.state.config.api.replicas : 1}
                    onChange={(event) => this.update('api', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Scheduler</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="number"
                    min="1"
                    value={this.state.config.scheduler ? this.state.config.scheduler.replicas : 1}
                    onChange={(event) => this.update('scheduler', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Hyper params search</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="number"
                    min="1"
                    value={this.state.config.hpsearch ? this.state.config.hpsearch.replicas : 1}
                    onChange={(event) => this.update('hpsearch', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Events Handlers</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="number"
                    min="1"
                    value={this.state.config.eventsHandlers ? this.state.config.eventsHandlers.replicas : 1}
                    onChange={(event) => this.update('eventsHandlers', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Event Monitors</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="number"
                    min="1"
                    value={this.state.config.eventMonitors ? this.state.config.eventMonitors.replicas : 1}
                    onChange={(event) => this.update('eventMonitors', event.target.value)}
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
