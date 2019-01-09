import * as _ from 'lodash';
import * as React from 'react';

import {
  AffinityInterface,
  AffinityStrInterface,
  ConfigInterface,
  NodeSelectorsInterface,
  NodeSelectorsStrInterface,
  TolerationsInterface,
  TolerationsStrInterface
} from '../../interfaces/config';
import PreviewForm from './previewForm';
import { checkArray, checkObj, parseYaml } from '../../libs/utils';

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
    const valueJson = parseYaml(value);

    if (_.isNil(config.nodeSelectors)) {
      config.nodeSelectors = {} as NodeSelectorsInterface;
    }
    if (_.isNil(config.nodeSelectorsStr)) {
      config.nodeSelectorsStr = {} as NodeSelectorsStrInterface;
    }

    if (key === 'core') {
      config.nodeSelectorsStr.core = value;
      if (checkObj(valueJson)) {
        delete config.nodeSelectors.core;
      } else {
        config.nodeSelectors.core = valueJson;
      }
    } else if (key === 'experiments') {
      config.nodeSelectorsStr.experiments = value;
      if (checkObj(valueJson)) {
        delete config.nodeSelectors.experiments;
      } else {
        config.nodeSelectors.experiments = valueJson;
      }
    } else if (key === 'jobs') {
      config.nodeSelectorsStr.jobs = value;
      if (checkObj(valueJson)) {
        delete config.nodeSelectors.jobs;
      } else {
        config.nodeSelectors.jobs = valueJson;
      }
    } else if (key === 'builds') {
      config.nodeSelectorsStr.builds = value;
      if (checkObj(valueJson)) {
        delete config.nodeSelectors.jobs;
      } else {
        config.nodeSelectors.builds = valueJson;
      }
    }
    this.setState({config});
  };

  public updateTolerations = (key: string, value: string) => {
    const config = _.cloneDeep(this.state.config);
    const valueJson = parseYaml(value);

    if (_.isNil(config.tolerationsStr)) {
      config.tolerationsStr = {} as TolerationsStrInterface;
    }
    if (_.isNil(config.tolerations)) {
      config.tolerations = {} as TolerationsInterface;
    }

    if (key === 'resourcesDaemon') {
      config.tolerationsStr.resourcesDaemon = value;
      if (checkArray(valueJson)) {
        delete config.tolerations.resourcesDaemon;
      } else {
        config.tolerations.resourcesDaemon = valueJson;
      }
    } else if (key === 'core') {
      config.tolerationsStr.core = value;
      if (checkArray(valueJson)) {
        delete config.tolerations.core;
      } else {
        config.tolerations.core = valueJson;
      }
    } else if (key === 'experiments') {
      config.tolerationsStr.experiments = value;
      if (checkArray(valueJson)) {
        delete config.tolerations.experiments;
      } else {
        config.tolerations.experiments = valueJson;
      }
    } else if (key === 'jobs') {
      config.tolerationsStr.jobs = value;
      if (checkArray(valueJson)) {
        delete config.tolerations.jobs;
      } else {
        config.tolerations.jobs = valueJson;
      }
    } else if (key === 'builds') {
      config.tolerationsStr.builds = value;
      if (checkArray(valueJson)) {
        delete config.tolerations.builds;
      } else {
        config.tolerations.builds = valueJson;
      }
    }
    this.setState({config});
  };

  public updateAffinity = (key: string, value: string) => {
    const config = _.cloneDeep(this.state.config);
    const valueJson = parseYaml(value);

    if (_.isNil(config.affinityStr)) {
      config.affinityStr = {} as AffinityStrInterface;
    }
    if (_.isNil(config.affinity)) {
      config.affinity = {} as AffinityInterface;
    }

    if (key === 'core') {
      config.affinityStr.core = value;
      if (checkObj(valueJson)) {
        delete config.affinity.core;
      } else {
        config.affinity.core = valueJson;
      }
    } else if (key === 'experiments') {
      config.affinityStr.experiments = value;
      if (checkObj(valueJson)) {
        delete config.affinity.experiments;
      } else {
        config.affinity.experiments = valueJson;
      }
    } else if (key === 'jobs') {
      config.affinityStr.jobs = value;
      if (checkObj(valueJson)) {
        delete config.affinity.jobs;
      } else {
        config.affinity.jobs = valueJson;
      }
    } else if (key === 'builds') {
      config.affinityStr.builds = value;
      if (checkObj(valueJson)) {
        delete config.affinity.builds;
      } else {
        config.affinity.builds = valueJson;
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
                <hr className="navbar-divider"/>
                <h6>Node selectors</h6>
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
                        value={this.state.config.nodeSelectorsStr ?
                          this.state.config.nodeSelectorsStr.core || '' :
                          ''}
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
                        value={this.state.config.nodeSelectorsStr ?
                          this.state.config.nodeSelectorsStr.experiments || '' :
                          ''}
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
                        value={this.state.config.nodeSelectorsStr ?
                          this.state.config.nodeSelectorsStr.jobs || '' :
                          ''}
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
                        value={this.state.config.nodeSelectorsStr ?
                          this.state.config.nodeSelectorsStr.builds || '' :
                          ''}
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
                <hr className="navbar-divider"/>
                <h6>Affinity</h6>
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
                        value={this.state.config.affinityStr ?
                          this.state.config.affinityStr.core || '' :
                          ''}
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
                        value={this.state.config.affinityStr ?
                          this.state.config.affinityStr.experiments || '' :
                          ''}
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
                        value={this.state.config.affinityStr ?
                          this.state.config.affinityStr.jobs || '' :
                          ''}
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
                        value={this.state.config.affinityStr ?
                          this.state.config.affinityStr.builds || '' :
                          ''}
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
                <hr className="navbar-divider"/>
                <h6>Tolerations</h6>
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
                        value={this.state.config.tolerationsStr ?
                          this.state.config.tolerationsStr.resourcesDaemon || '' :
                          ''}
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
                        value={this.state.config.tolerationsStr ?
                          this.state.config.tolerationsStr.core || '' :
                          ''}
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
                        value={this.state.config.tolerationsStr ?
                          this.state.config.tolerationsStr.experiments || ''
                          : ''}
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
                        value={this.state.config.tolerationsStr ?
                          this.state.config.tolerationsStr.jobs || '' :
                          ''}
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
                        value={this.state.config.tolerationsStr ?
                          this.state.config.tolerationsStr.builds || '' :
                          ''}
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
