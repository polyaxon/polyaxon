import * as _ from 'lodash';
import * as React from 'react';

export interface Props {
  outputsFile: string;
}

export interface State {
  outputsFile: string;
}

export default class OutputsImg extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      outputsFile: this.props.outputsFile,
    };
  }

  public componentDidUpdate(prevProps: Props, prevState: {}) {
    if (!_.isEqual(this.props.outputsFile, prevProps.outputsFile)) {
      this.setState({
        ...prevState,
        outputsFile: this.props.outputsFile,
      });
    }
  }

  public render() {
    return (
      <div className="outputsFile">
        <img src={this.state.outputsFile} />
      </div>
    );
  }

}
