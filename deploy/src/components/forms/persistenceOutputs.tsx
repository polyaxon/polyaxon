import * as _ from 'lodash';
import * as React from 'react';

import { PersistenceDefInterface, PersistenceInterface } from '../../interfaces/config';
import { ConfigInterface } from '../../interfaces/config';
import PersistenceDefList from './persistenceDefList';
import PreviewForm from './previewForm';

export interface Props {
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
  updateConfig: (config: ConfigInterface) => void;
}

interface State {
  config: ConfigInterface;
}

export default class PersistenceOutputs extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      config: this.props.config,
    };
    this.state.config.persistence = this.state.config.persistence || {outputs: {}} as PersistenceInterface;
    this.state.config.persistence.outputs = this.state.config.persistence.outputs || {} as {[key: string]: PersistenceDefInterface};
  }

  public update = (persistence: { [key: string]: PersistenceDefInterface }) => {
    const config = _.cloneDeep(this.state.config);
    if (_.isNil(config.persistence) || _.isNil(config.persistence.outputs)) {
      config.persistence = {outputs: persistence} as PersistenceInterface;
    } else {
      config.persistence.outputs = persistence;
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
      const config: { [key: string]: PersistenceDefInterface } = {};
      if (!_.isNil(this.state.config.persistence) &&
          !_.isNil(this.state.config.persistence.outputs)) {
        for (const key of Object.keys(this.state.config.persistence.outputs)) {
          config[key] = {} as PersistenceDefInterface;

          if (!_.isNil(this.state.config.persistence.outputs[key].existingClaim)) {
            config[key].existingClaim = this.state.config.persistence.outputs[key].existingClaim;
          }

          if (!_.isNil(this.state.config.persistence.outputs[key].mountPath)) {
            config[key].mountPath = this.state.config.persistence.outputs[key].mountPath;
          }

          if (!_.isNil(this.state.config.persistence.outputs[key].hostPath)) {
            config[key].hostPath = this.state.config.persistence.outputs[key].hostPath;
          }

          if (!_.isNil(this.state.config.persistence.outputs[key].readonly)) {
            config[key].readonly = this.state.config.persistence.outputs[key].readonly;
          }
        }
      }

      return config;
    };

    const defaultConfig = this.props.defaultConfig.defaultPersistence ? this.props.defaultConfig.defaultPersistence.outputs : {};

    return (
      <div className="columns">
        <div className="column is-7">
          {!_.isNil(this.state.config.persistence) &&
          <PersistenceDefList config={this.state.config.persistence.outputs} updateConfig={this.update} naming="outputs"/>
          }
        </div>
        <PreviewForm currentConfig={currentConfig()} defaultConfig={defaultConfig}/>
      </div>
    );
  }
}
