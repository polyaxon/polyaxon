import * as _ from 'lodash';
import * as React from 'react';

export interface Props {
  outputsFile: string;
}

export default class OutputsImg extends React.Component<Props, {}> {

  public shouldComponentUpdate(prevProps: Props, prevState: {}) {
    return !_.isEqual(this.props.outputsFile, prevProps.outputsFile);
  }

  public render() {
    return (
      <div className="outputs-file">
        <img src={this.props.outputsFile} className="img-responsive" />
      </div>
    );
  }

}
