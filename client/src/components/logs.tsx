import * as React from 'react';

import Refresh from './refresh';

import './logs.less';

export interface Props {
  logs: string;
  fetchData: () => any;
}

export default class Logs extends React.Component<Props, {}> {

  public componentDidMount() {
    this.props.fetchData();
  }

  public refresh = () => {
    this.props.fetchData();
  };

  public render() {
    const logs = this.props.logs;
    const logsElements = logs.length > 0 ?
      (logs.split('\n').map((line, i) => <p key={i}>{line}</p>)) :
      (<p>No logs</p>);

    return (
      <div className="logs">
        <div className="row">
          <div className="col-md-12 button-refresh-alone">
            <Refresh callback={this.refresh} pullRight={true}/>
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
