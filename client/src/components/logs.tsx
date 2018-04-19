import * as React from 'react';

export interface Props {
  logs: string[];
  fetchData: () => any;
}

export default class Logs extends React.Component<Props, Object> {

  componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    let logs: string[] = [];
    for (let i = 1; i < 10; i++) {
      logs.push('This is a log message');
    }
    logs = this.props.logs;
    return (
      <div className="row">
        {logs.map(line => <p>{line}</p>)}
      </div>
    );
  }
}
