import * as _ from 'lodash';
import * as React from 'react';

import {
  ConfigInterface,
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

export default class Registries extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      config: this.props.config,
    };
  }

  public update = (value: string) => {
    const config = _.cloneDeep(this.state.config);
    const valueJson = parseYaml(value);

    if (_.isNil(config.privateRegistries)) {
      config.privateRegistries = [];
    }

    config.privateRegistriesStr = value;
    if (checkArray(valueJson)) {
      delete config.privateRegistries;
    } else {
      config.privateRegistries = valueJson;
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
      if (!_.isNil(this.state.config.privateRegistries)) {
        config.privateRegistries = this.state.config.privateRegistries;
      }
      return config;
    };

    const defaultIntegrationsConfig = {
      privateRegistries: this.props.defaultConfig.privateRegistries,
    };

    return (
      <div className="columns">
        <div className="column">
          <div className="columns">
            <div className="column is-7">
              <div className="field is-horizontal">
                <div className="field-label is-normal">
                  <label className="label">Private Registries</label>
                </div>
                <div className="field-body">
                  <div className="field">
                    <div className="control">
                      <textarea
                        className="textarea"
                        rows={2}
                        value={this.state.config.privateRegistriesStr || ''}
                        onChange={(event) => this.update(event.target.value)}
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
