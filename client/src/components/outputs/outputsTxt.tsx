import * as _ from 'lodash';
import * as React from 'react';

import CodeTable from '../tables/codeTable';

export interface Props {
  outputsFile: string;
}

export default class OutputsTxt extends React.Component<Props, {}> {

  public shouldComponentUpdate(prevProps: Props, prevState: {}) {
    return !_.isEqual(this.props.outputsFile, prevProps.outputsFile);
  }

  public render() {
    return (
      <div className="outputs-file">
        <CodeTable lines={this.props.outputsFile.split('\n')}/>
      </div>
    );
  }

}
