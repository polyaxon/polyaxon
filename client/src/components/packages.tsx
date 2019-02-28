import * as React from 'react';

import CodeTable from './tables/codeTable';

export interface Props {
  runEnv: { [key: string]: any };
}

export default class Packages extends React.Component<Props, {}> {
  public render() {
    return (
      <div>
        {this.props.runEnv.packages &&
        <CodeTable lines={this.props.runEnv.packages}/>
        }
      </div>
    );
  }
}
