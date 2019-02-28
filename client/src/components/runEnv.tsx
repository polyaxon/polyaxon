import * as React from 'react';

import VerticalTable from './tables/verticalTable';

export interface Props {
  runEnv: { [key: string]: any };
}

export default class RunEnv extends React.Component<Props, {}> {
  public render() {
    const runEnv = this.props.runEnv;
    let keys: string[] = [];
    if ('client_version' in runEnv && 'python_version' in runEnv) {
      keys = [
        'client_version',
        'is_notebook',
        'filename',
        'module_path',
        'os',
        'system',
        'python_version',
        'sys.argv'
      ];
    } else {
      keys = Object.keys(runEnv).sort();
    }

    return (
      <VerticalTable values={this.props.runEnv} keys={keys}/>
    );
  }
}
