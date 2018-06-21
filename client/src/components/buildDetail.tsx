import * as React from 'react';
import * as _ from 'lodash';

import { BuildModel } from '../models/build';

export interface Props {
  build: BuildModel;
  onDelete: () => any;
  fetchData: () => any;
}

export default class BuildDetail extends React.Component<Props, Object> {
  componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const build = this.props.build;
    if (_.isNil(build)) {
      return (<div>Nothing</div>);
    }
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <a className="back-button" onClick={() => {window.history.back(); }}>&#060;</a>
            <span className="title">
              <i className="fa fa-cube icon" aria-hidden="true"/>
              {build.unique_name}
            </span>
            <span className="description">
              <pre>{JSON.stringify(build.definition, null, 2)}</pre>
            </span>
          </div>
        </div>
      </div>
    );
  }
}
