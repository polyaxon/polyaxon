import * as React from 'react';
import * as _ from 'lodash';

import { JobModel } from '../models/job';

export interface Props {
  job: JobModel;
  onDelete: (job: JobModel) => any;
  fetchData: () => any;
}

export default class JobDetail extends React.Component<Props, Object> {
  componentDidMount() {
    const {job, onDelete, fetchData} = this.props;
    fetchData();
  }

  public render() {
    const {job, onDelete, fetchData} = this.props;
    if (_.isNil(job)) {
      return (<div>Nothing</div>);
    }
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <a className="back-button" onClick={() => {window.history.back(); }}>&#060;</a>
            <span className="title">
              <i className="fa fa-cube icon" aria-hidden="true"/>
              {job.unique_name}
            </span>
            <span className="description">
              <pre>{JSON.stringify(job.definition, null, 2)}</pre>
            </span>
          </div>
        </div>
      </div>
    );
  }
}
