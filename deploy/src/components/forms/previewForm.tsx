import * as jsYaml from 'js-yaml';
import * as React from 'react';

export interface Props {
  currentConfig: { [key: string]: any; };
  defaultConfig: { [key: string]: any; };
}

export default class PreviewForm extends React.Component<Props, {}> {
  public render() {
    return (
      <div className="column is-5 preview">
        <div className="columns">
          <div className="column">
            <div className="content">
              <h4> Preview Override config </h4>
              <figure className="content-figure">
                <pre className="content content-output content-preview">
                  <p>{jsYaml.dump(this.props.currentConfig)}</p>
                  </pre>
              </figure>
            </div>
          </div>
        </div>
        <div className="columns">
          <div className="column">
            <div className="content">
              <h4> Default config Section </h4>
              <figure className="content-figure">
                <pre className="content content-output content-preview">
                  <p>{jsYaml.dump(this.props.defaultConfig)}</p>
                </pre>
              </figure>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
