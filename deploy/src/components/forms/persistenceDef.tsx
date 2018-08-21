import * as _ from 'lodash';
import * as React from 'react';

import { PersistenceDefInterface } from '../../interfaces/config';

export interface Props {
  config: PersistenceDefInterface;
  updateConfig: (config: PersistenceDefInterface) => void;
  useReadOnly: boolean;
}

interface State {
  config: PersistenceDefInterface;
}

export default class PersistenceDef extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      config: this.props.config,
    };
  }

  public updatePersistence = (key: string, value: string) => {
    let config = _.cloneDeep(this.state.config);
    if (_.isNil(config)) {
      config = {} as PersistenceDefInterface;
    }
    if (key === 'existingClaim') {
      config.existingClaim = value;
      delete config.hostPath;
    } else if (key === 'hostPath') {
      config.hostPath = value;
      delete config.existingClaim;
    } else if (key === 'mountPath') {
      config.mountPath = value;
    }
    this.setState({config});
  };

  public updatePersistenceReadOnly = (value: boolean) => {
    const config = _.cloneDeep(this.state.config);
    config.readonly = value;
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
                    value={this.state.config.existingClaim || ''}
                    onChange={(event) => this.updatePersistence('existingClaim', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Mount Path</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={this.state.config.mountPath || ''}
                    onChange={(event) => this.updatePersistence('mountPath', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Host Path</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <input
                    className="input"
                    type="text"
                    value={this.state.config.hostPath || ''}
                    onChange={(event) => this.updatePersistence('hostPath', event.target.value)}
                  />
                </div>
              </div>
            </div>
          </div>
          {this.props.useReadOnly &&
          <div className="field is-horizontal">
            <div className="field-label is-normal">
              <label className="label">Read only</label>
            </div>
            <div className="field-body">
              <div className="field">
                <div className="control">
                  <div className="field-body">
                    <input
                      type="checkbox"
                      onChange={(event) => this.updatePersistenceReadOnly(event.target.checked)}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
          }
        </div>
      </div>
    );
  }
}
