import * as jsYaml from 'js-yaml';
import * as React from 'react';

export interface Props {
  currentConfig: { [key: string]: any; };
  defaultConfig: { [key: string]: any; };
}

export default class PreviewForm extends React.Component<Props, Object> {
  public render() {
    return (
      <div className="column is-5 preview">
        <div className="columns">
          <div className="column">
            <div className="content">
              <h4> Preview Override config </h4>
              <p>
                {jsYaml.dump(this.props.currentConfig)}
              </p>
            </div>
          </div>
        </div>
        <div className="columns">
          <div className="column">
            <div className="content">
              <h4> Default config Section </h4>
              <p>
                {jsYaml.dump(this.props.defaultConfig)}
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
