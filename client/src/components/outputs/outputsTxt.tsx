import * as _ from 'lodash';
import * as React from 'react';

import CodeTable from '../tables/codeTable';

export interface Props {
  outputsFile: string;
}

export interface State {
  outputsFile: string;
}

export default class OutputsTxt extends React.Component<Props, State> {
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
        <CodeTable lines={this.state.outputsFile.split('\n')}/>
      </div>
    );
  }

}
