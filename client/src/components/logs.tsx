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

export interface State {
  logsOnly: boolean;
}

export default class Logs extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      logsOnly: false
    };
  }

  public componentDidMount() {
    this.props.fetchData();
  }

  public refresh = () => {
    this.props.fetchData();
  };

  public updateLogs = () => {
    this.setState((prevState, prevProps) => ({
      ...prevState, logsOnly: !prevState.logsOnly
    }));
  };

  public render() {
    const lineRegex = /(\d{2}(?:\d{2})?-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2}\s\w+\s(?:\w+\s)?(?:\w+\.\d\s)?--\s)/;
    const formatLogs = (line: string) => {
      const values = line.split(lineRegex);
      if (values.length === 3) {
        if ( this.state.logsOnly ) {
          return (<span>{values[2]}</span>);
        } else {
          return (<span><span className="logs-info">{values[1]}</span>{values[2]}</span>);
        }
      }
      return line;
    };
    const logs = this.props.logs;
    const logsElements = logs.length > 0 ?
      (logs.split(/\r|\n/).map((line, i) => <p key={i}>{formatLogs(line)}</p>)) :
      (<p>No logs</p>);

    return (
      <div className="logs">
        <div className="row">
          <div className="col-md-12 button-group-tools button-refresh-alone">
            <Refresh callback={this.refresh} pullRight={true}/>
            <div className="pull-right">
            <span>
              <button
                onClick={() => this.updateLogs()}
                className="btn btn-sm btn-default"
              >
                {this.state.logsOnly
                  ? <><i className="fa fa-plus-square icon" aria-hidden="true"/> Add info</>
                  : <><i className="fa fa-minus-square icon" aria-hidden="true"/> Logs Only</>
                }
              </button>
            </span>
            </div>
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
