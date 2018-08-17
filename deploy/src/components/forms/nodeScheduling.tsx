import * as _ from 'lodash';
import * as React from 'react';

import {
  AffinityInterface,
  ConfigInterface,
  NodeSelectorsInterface,
  TolerationsInterface
} from '../../interfaces/config';
import PreviewForm from './previewForm';

export interface Props {
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
  updateConfig: (config: ConfigInterface) => void;
}

interface State {
  config: ConfigInterface;
}

export default class NodeScheduling extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      config: this.props.config,
    };
  }

  public updateNodeSelectors = (key: string, value: string) => {
    const config = _.cloneDeep(this.state.config);

    if (_.isNil(config.nodeSelectors)) {
      config.nodeSelectors = {} as NodeSelectorsInterface;
    }
    if (key === 'core') {
      config.nodeSelectors.core = value;
    } else if (key === 'experiments') {
      config.nodeSelectors.experiments = value;
    } else if (key === 'jobs') {
      config.nodeSelectors.jobs = value;
    } else if (key === 'builds') {
      config.nodeSelectors.builds = value;
    }
    this.setState({config});
  };

  public updateTolerations = (key: string, value: string) => {
    const config = _.cloneDeep(this.state.config);

    if (_.isNil(config.tolerations)) {
      config.tolerations = {} as TolerationsInterface;
    }
    if (key === 'resourcesDaemon') {
      config.tolerations.resourcesDaemon = value;
    } else if (key === 'core') {
      config.tolerations.experiments = value;
    } else if (key === 'experiments') {
      config.tolerations.experiments = value;
    } else if (key === 'jobs') {
      config.tolerations.jobs = value;
    } else if (key === 'builds') {
      config.tolerations.builds = value;
    }
    this.setState({config});
  };

  public updateAffinity = (key: string, value: string) => {
    const config = _.cloneDeep(this.state.config);

    if (_.isNil(config.affinity)) {
      config.affinity = {} as AffinityInterface;
    }
    if (key === 'core') {
      config.affinity.core = value;
    } else if (key === 'experiments') {
      config.affinity.experiments = value;
    } else if (key === 'jobs') {
      config.affinity.jobs = value;
    } else if (key === 'builds') {
      config.affinity.builds = value;
    }
    this.setState({config});
  };

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (!_.isEqual(this.state.config, prevState.config)) {
      this.props.updateConfig(this.state.config);
    }
  }

  public render() {
    const currentNodeSelectorsConfig = () => {
      const config: ConfigInterface = {};
      if (!_.isNil(this.state.config.nodeSelectors)) {
        config.nodeSelectors = this.state.config.nodeSelectors;
      }
      return config;
    };

    const defaultNodeSelectorsConfig = {
      nodeSelectors: this.props.defaultConfig.nodeSelectors,
    };

    const currentAffinityConfig = () => {
      const config: ConfigInterface = {};
      if (!_.isNil(this.state.config.affinity)) {
        config.affinity = this.state.config.affinity;
      }
      return config;
    };

    const defaultAffinityConfig = {
      affinity: this.props.defaultConfig.affinity,
    };

    const currentTolerationsConfig = () => {
      const config: ConfigInterface = {};
      if (!_.isNil(this.state.config.tolerations)) {
        config.tolerations = this.state.config.tolerations;
      }
      return config;
    };

    const defaultTolerationsConfig = {
      tolerations: this.props.defaultConfig.tolerations,
    };

    return (
      <div className="columns">
        <div className="column">
          <div className="columns">
            <div className="column is-7">
              <div className="content">
                <h4>Node selectors</h4>
                <hr className="navbar-divider"/>
              </div>
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Core</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <input
                        className="input"
                        type="text"
                        value={this.state.config.nodeSelectors ? this.state.config.nodeSelectors.core || '' : ''}
                        onChange={(event) => this.updateNodeSelectors('core', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Experiments</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <input
                        className="input"
                        type="text"
                        value={this.state.config.nodeSelectors ? this.state.config.nodeSelectors.experiments || '' : ''}
                        onChange={(event) => this.updateNodeSelectors('experiments', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Jobs</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <input
                        className="input"
                        type="text"
                        value={this.state.config.nodeSelectors ? this.state.config.nodeSelectors.jobs || '' : ''}
                        onChange={(event) => this.updateNodeSelectors('jobs', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Builds</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <input
                        className="input"
                        type="text"
                        value={this.state.config.nodeSelectors ? this.state.config.nodeSelectors.builds || '' : ''}
                        onChange={(event) => this.updateNodeSelectors('builds', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <PreviewForm
              currentConfig={currentNodeSelectorsConfig()}
              defaultConfig={defaultNodeSelectorsConfig}
            />
          </div>

          <div className="columns">
            <div className="column is-7">
              <div className="content">
                <h4>Affinity</h4>
                <hr className="navbar-divider"/>
              </div>
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Core</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <textarea
                        className="textarea"
                        rows={2}
                        value={this.state.config.affinity ? this.state.config.affinity.core || '' : ''}
                        onChange={(event) => this.updateAffinity('core', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Experiments</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <textarea
                        className="textarea"
                        rows={2}
                        value={this.state.config.affinity ? this.state.config.affinity.experiments || '' : ''}
                        onChange={(event) => this.updateAffinity('experiments', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Jobs</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <textarea
                        className="textarea"
                        rows={2}
                        value={this.state.config.affinity ? this.state.config.affinity.jobs || '' : ''}
                        onChange={(event) => this.updateAffinity('jobs', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Builds</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <textarea
                        className="textarea"
                        rows={2}
                        value={this.state.config.affinity ? this.state.config.affinity.builds || '' : ''}
                        onChange={(event) => this.updateAffinity('builds', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <PreviewForm
              currentConfig={currentAffinityConfig()}
              defaultConfig={defaultAffinityConfig}
            />
          </div>

          <div className="columns">
            <div className="column is-7">
              <div className="content">
                <h4>Tolerations</h4>
                <hr className="navbar-divider"/>
              </div>
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Resources Daemon</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <textarea
                        className="textarea"
                        rows={2}
                        value={this.state.config.tolerations ? this.state.config.tolerations.resourcesDaemon || '' : ''}
                        onChange={(event) => this.updateTolerations('resourcesDaemon', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Core</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <textarea
                        className="textarea"
                        rows={2}
                        value={this.state.config.tolerations ? this.state.config.tolerations.core || '' : ''}
                        onChange={(event) => this.updateTolerations('core', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Experiments</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <textarea
                        className="textarea"
                        rows={2}
                        value={this.state.config.tolerations ? this.state.config.tolerations.experiments || '' : ''}
                        onChange={(event) => this.updateTolerations('experiments', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Jobs</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <textarea
                        className="textarea"
                        rows={2}
                        value={this.state.config.tolerations ? this.state.config.tolerations.jobs || '' : ''}
                        onChange={(event) => this.updateTolerations('jobs', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Builds</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <textarea
                        className="textarea"
                        rows={2}
                        value={this.state.config.tolerations ? this.state.config.tolerations.builds || '' : ''}
                        onChange={(event) => this.updateTolerations('builds', event.target.value)}
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <PreviewForm
              currentConfig={currentTolerationsConfig()}
              defaultConfig={defaultTolerationsConfig}
            />
          </div>
        </div>
      </div>
    );
  }
}
