import * as _ from 'lodash';
import * as React from 'react';

import { PersistenceDefInterface, PersistenceInterface } from '../../interfaces/config';
import { ConfigInterface } from '../../interfaces/config';
import PersistenceDef from './persistenceDef';
import PreviewForm from './previewForm';

export interface Props {
  config: ConfigInterface;
  defaultConfig: ConfigInterface;
  updateConfig: (config: ConfigInterface) => void;
}

interface State {
  config: ConfigInterface;
}

export default class PersistenceLogs extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      config: this.props.config,
    };
    this.state.config.persistence = this.state.config.persistence || {logs: {}} as PersistenceInterface;
    this.state.config.persistence.logs = this.state.config.persistence.logs || {} as PersistenceDefInterface;
  }

  public update = (persistence: PersistenceDefInterface) => {
    const config = _.cloneDeep(this.state.config);
    if (_.isNil(config.persistence) || _.isNil(config.persistence.logs)) {
      config.persistence = {logs: persistence} as PersistenceInterface;
    } else {
      config.persistence.logs = persistence;
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
      const config: PersistenceDefInterface = {};
      if (!_.isNil(this.state.config.persistence) &&
        !_.isNil(this.state.config.persistence.logs) &&
        !_.isNil(this.state.config.persistence.logs.existingClaim)) {
        config.existingClaim = this.state.config.persistence.logs.existingClaim;
      }

      if (!_.isNil(this.state.config.persistence) &&
        !_.isNil(this.state.config.persistence.logs) &&
        !_.isNil(this.state.config.persistence.logs.mountPath)) {
        config.mountPath = this.state.config.persistence.logs.mountPath;
      }

      if (!_.isNil(this.state.config.persistence) &&
        !_.isNil(this.state.config.persistence.logs) &&
        !_.isNil(this.state.config.persistence.logs.hostPath)) {
        config.hostPath = this.state.config.persistence.logs.hostPath;
      }

      if (!_.isNil(this.state.config.persistence) &&
        !_.isNil(this.state.config.persistence.logs) &&
        !_.isNil(this.state.config.persistence.logs.readonly)) {
        config.readonly = this.state.config.persistence.logs.readonly;
      }

      return config;
    };

    const defaultConfig = this.props.defaultConfig.persistence ? this.props.defaultConfig.persistence.logs : {};

    return (
      <div className="columns">
        <div className="column is-7">
          {!_.isNil(this.state.config.persistence) &&
          <PersistenceDef
            config={this.state.config.persistence.logs}
            updateConfig={this.update}
            useReadOnly={false}
          />
          }
        </div>
        <PreviewForm currentConfig={currentConfig()} defaultConfig={defaultConfig}/>
      </div>
    );
  }
}
