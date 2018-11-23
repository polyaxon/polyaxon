import * as React from 'react';

import Download from './download';
import Refresh from './refresh';

import './logs.less';

export interface Props {
  logs: string;
  fetchData: () => any;
  downloadLogsUrl: string;
  downloadLogsName: string;
}

export default class Logs extends React.Component<Props, {}> {

  public componentDidMount() {
    this.props.fetchData();
  }

  public refresh = () => {
    this.props.fetchData();
  };

  public render() {
    const lineRe = /(\d{2}(?:\d{2})?-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}\s\w+\s)/;
    const formatLogs = (line: string) => {
      const values = line.split(lineRe);
      if (values.length === 3) {
        return (<span><span className="timestamp">{values[1]}</span>{values[2]}</span>);
      }
      return line;
    };
    const logs = this.props.logs;
    const logsElements = logs.length > 0 ?
      (logs.split('\n').map((line, i) => <p key={i}>{formatLogs(line)}</p>)) :
      (<p>No logs</p>);

    return (
      <div className="logs">
        <div className="row">
          <div className="col-md-12 button-group-tools button-refresh-alone">
            <Refresh callback={this.refresh} pullRight={true}/>
            <Download
              name={`${this.props.downloadLogsName}.txt`}
              url={this.props.downloadLogsUrl}
              pullRight={true}
            />
          </div>
        </div>
        <div className="row">
          <div className="col-md-12">
            <div className="logs-header">
              Logs
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-md-12">
            <div className="logs-content">
              {logsElements}
            </div>
          </div>
        </div>
      </div>

    );
  }
}
