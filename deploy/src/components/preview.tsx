import * as jsYaml from 'js-yaml';
import * as React from 'react';

import { ConfigInterface } from '../interfaces/config';

export interface Props {
  config?: ConfigInterface;
}

export interface State {
  json: boolean;
}

export default class Preview extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      json: false,
    };
  }

  public render() {
    return (
      <div className="columns preview">
        <div className="column is-8 is-offset-2">
          <div className="content">
            <p>
              {this.state.json ?
                JSON.stringify(this.props.config, null, ' ') :
                jsYaml.dump(this.props.config)}
            </p>
          </div>
        </div>
      </div>
    );
  }
}
