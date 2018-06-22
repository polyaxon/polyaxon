import * as React from 'react';
import * as _ from 'lodash';

import { JobModel } from '../models/job';
import Logs from '../containers/logs';
import {
  getJobUrl,
  getProjectUrl,
  getUserUrl,
  splitUniqueName,
} from '../constants/utils';
import Breadcrumb from './breadcrumb';
import LinkedTab from './linkedTab';
import JobOverview from './jobOverview';

export interface Props {
  job: JobModel;
  onDelete: () => any;
  fetchData: () => any;
}

export default class JobDetail extends React.Component<Props, Object> {
  componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const job = this.props.job;
    if (_.isNil(job)) {
      return (<div>Nothing</div>);
    }
    let values = splitUniqueName(job.project);
    let jobUrl = getJobUrl(values[0], values[1], this.props.job.id);
    let breadcrumbLinks = [
      {name: values[0], value: getUserUrl(values[0])},
      {name: values[1], value: getProjectUrl(values[0], values[1])},
      {name: `Job ${job.id}`}];
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <Breadcrumb icon="fa-cube" links={breadcrumbLinks}/>
            <LinkedTab
              baseUrl={jobUrl}
              tabs={[
                {
                  title: 'Overview',
                  component: <JobOverview job={job}/>,
                  relUrl: ''
                }, {
                  title: 'Logs',
                  component: <Logs
                    fetchData={() => null}
                    logs={''}
                    user={job.user}
                    project={job.project}
                    resource="jobs"
                    id={job.id}
                  />,
                  relUrl: 'logs'
                }
              ]}
            />
          </div>
        </div>
      </div>
    );
  }
}
