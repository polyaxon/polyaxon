import * as React from 'react';

import './logs.less';

export interface Props {
  logs: string;
  fetchData: () => any;
}

export default class Logs extends React.Component<Props, Object> {

  componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const logs = this.props.logs;
    let logsElements = logs.length > 0 ?
      (logs.split('\n').map((line, i) => <p key={i}>{line}</p>)) :
      (<p>No logs</p>);

    return (
      <div className="logs">
        {logsElements}
      </div>
    );
  }
}
