import * as _ from 'lodash';
import * as React from 'react';

import { ResourcesInterface } from '../../interfaces/config';

export interface Props {
  config: ResourcesInterface;
  updateConfig: (config: ResourcesInterface) => void;
  name: string;
}

interface State {
  config: ResourcesInterface;
}

export default class Resources extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      config: this.props.config || {limits: {}, requests: {}},
    };
  }

  public updateLimits = (value: { [key: string]: string }) => {
    const config = _.cloneDeep(this.state.config);
    config.limits = {...config.limits, ...value};
    this.setState({config});
  };

  public updateRequests = (value: { [key: string]: string }) => {
    const config = _.cloneDeep(this.state.config);
    config.requests = {...config.requests, ...value};
    this.setState({config});
  };

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (!_.isEqual(this.state.config, prevState.config)) {
      this.props.updateConfig(this.state.config);
    }
  }

  public render() {
    return (
      <div className="columns">
        <div className="column">
          <div className="content">
            <hr className="navbar-divider"/>
            <h6>{this.props.name} resources</h6>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Limits cpu</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={this.state.config.limits.cpu || ''}
                    onChange={(event) => this.updateLimits({cpu: event.target.value})}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Limits memory</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={this.state.config.limits.memory || ''}
                    onChange={(event) => this.updateLimits({memory: event.target.value})}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Requests cpu</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={this.state.config.requests.cpu || ''}
                    onChange={(event) => this.updateRequests({cpu: event.target.value})}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Requests memory</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={this.state.config.requests.memory || ''}
                    onChange={(event) => this.updateRequests({memory: event.target.value})}
                  />
                </div>
              </div>
            </div>
          </div>
          <hr className="navbar-divider"/>
        </div>
      </div>
    );
  }
}
