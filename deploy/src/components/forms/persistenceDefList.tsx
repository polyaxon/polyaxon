import * as _ from 'lodash';
import * as React from 'react';

import { PersistenceDefInterface } from '../../interfaces/config';
import PersistenceDef from './persistenceDef';

export interface Props {
  config: { [key: string]: PersistenceDefInterface };
  updateConfig: (config: { [key: string]: PersistenceDefInterface }) => void;
  naming: string;
}

interface State {
  config: { [key: string]: PersistenceDefInterface };
}

export default class PersistenceDefList extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      config: this.props.config,
    };
  }

  public addPersistence = () => {
    let config = _.cloneDeep(this.state.config);
    if (_.isNil(config)) {
      config = {};
    }
    const persistenceName = this.props.naming + (Object.keys(this.state.config).length + 1);
    config[persistenceName] = {} as PersistenceDefInterface;
    this.setState({config});
  };

  public RemovePersistence = (key: string) => {
    const config = _.cloneDeep(this.state.config);
    delete config[key];
    this.setState({config});
  };

  public update = (key: string, persistence: PersistenceDefInterface) => {
    this.state.config[key] = persistence;
    this.props.updateConfig(this.state.config);
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
          <div className="columns">
            <div className="column">
              <button className="button" onClick={(event) => this.addPersistence()}>
                <span className="icon is-small">
                  <i className="fas fa-plus"/>
                </span>
              </button>
            </div>
          </div>
          {Object.keys(this.state.config).map((key, idx) => (
              <div className="columns" key={idx}>
                <div className="column">
                  <div className="content">
                    <hr className="navbar-divider"/>
                    <h6>{key}
                    <a
                      className="delete is-pulled-right"
                      onClick={(event) => this.RemovePersistence(key)}
                    />
                    </h6>
                  </div>
                  <PersistenceDef
                    config={this.state.config[key]}
                    updateConfig={(persistence) => this.update(key, persistence)}
                    useReadOnly={true}
                  />
                </div>
              </div>
            )
          )}
        </div>
      </div>
    );
  }
}
