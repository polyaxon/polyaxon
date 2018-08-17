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

export default class PersistenceUpload extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      config: this.props.config,
    };
    this.state.config.persistence = this.state.config.persistence || {repos: {}} as PersistenceInterface;
    this.state.config.persistence.upload = this.state.config.persistence.upload || {} as PersistenceDefInterface;
  }

  public update = (persistence: PersistenceDefInterface) => {
    const config = _.cloneDeep(this.state.config);
    if (_.isNil(config.persistence) || _.isNil(config.persistence.upload)) {
      config.persistence = {upload: persistence} as PersistenceInterface;
    } else {
      config.persistence.upload = persistence;
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
          !_.isNil(this.state.config.persistence.upload) &&
          !_.isNil(this.state.config.persistence.upload.existingClaim)) {
        config.existingClaim = this.state.config.persistence.upload.existingClaim;
      }

      if (!_.isNil(this.state.config.persistence) &&
          !_.isNil(this.state.config.persistence.upload) &&
          !_.isNil(this.state.config.persistence.upload.mountPath)) {
        config.mountPath = this.state.config.persistence.upload.mountPath;
      }

      if (!_.isNil(this.state.config.persistence) &&
          !_.isNil(this.state.config.persistence.upload) &&
          !_.isNil(this.state.config.persistence.upload.hostPath)) {
        config.hostPath = this.state.config.persistence.upload.hostPath;
      }

      if (!_.isNil(this.state.config.persistence) &&
          !_.isNil(this.state.config.persistence.upload) &&
          !_.isNil(this.state.config.persistence.upload.readonly)) {
        config.readonly = this.state.config.persistence.upload.readonly;
      }

      return config;
    };

    const defaultConfig = this.props.defaultConfig.persistence ? this.props.defaultConfig.persistence.upload : {};

    return (
      <div className="columns">
        <div className="column is-7">
          {!_.isNil(this.state.config.persistence) &&
          <PersistenceDef
            config={this.state.config.persistence.upload}
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
