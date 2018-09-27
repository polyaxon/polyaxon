import * as _ from 'lodash';
import * as React from 'react';

import { EmptyList } from './empty/emptyList';
import CodeTable from './tables/codeTable';
import VerticalTable from './tables/verticalTable';

export interface Props {
  runEnv: { [key: string]: any };
}

export default class RunEnv extends React.Component<Props, {}> {
  public render() {
    const runEnv = this.props.runEnv;

    if (_.isNil(runEnv)) {
      return (
        <div className="row">
          <div className="col-md-12">
            {EmptyList(false, 'run environment', '')}
          </div>
        </div>
      );
    }

    let keys: string[] = [];
    if ('client_version' in runEnv && 'python_version' in runEnv) {
      keys = [
        'in_cluster',
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
      <div>
        <div className="row">
          <div className="col-md-8">
            <VerticalTable values={this.props.runEnv} keys={keys}/>
          </div>
        </div>
        {this.props.runEnv.packages &&
        <div className="row">
          <div className="col-md-12">
            <div className="meta meta-packages">
                <span className="meta-info">
                  <i className="fa fa-file-archive-o icon" aria-hidden="true"/>
                  <span className="title">Packages:</span>
                </span>
              <CodeTable lines={this.props.runEnv.packages}/>
            </div>
          </div>
        </div>
        }
      </div>
    );
  }
}
