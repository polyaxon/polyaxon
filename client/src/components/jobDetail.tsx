import * as React from 'react';
import * as _ from 'lodash';

import { JobModel } from '../models/job';
import Logs from '../containers/logs';
import Statuses from '../containers/statuses';
import {
  getJobUrl,
  getProjectUrl,
  getUserUrl,
  splitUniqueName,
} from '../constants/utils';
import Breadcrumb from './breadcrumb';
import LinkedTab from './linkedTab';
import JobOverview from './jobOverview';
import EntityBuild from '../containers/EntityBuild';
import { EmptyList } from './emptyList';
import JobInstructions from './instructions/jobInstructions';

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
      return EmptyList(false, 'job', 'job');
    }
    let values = splitUniqueName(job.project);
    let jobUrl = getJobUrl(values[0], values[1], this.props.job.id);
    let projectUrl = getProjectUrl(values[0], values[1]);
    let breadcrumbLinks = [
      {name: values[0], value: getUserUrl(values[0])},
      {name: values[1], value: projectUrl},
      {name: 'Jobs', value: `${projectUrl}#jobs`},
      {name: `Job ${job.id}`}];
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <Breadcrumb icon="fa-tasks" links={breadcrumbLinks}/>
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
                }, {
                  title: 'Build',
                  component: <EntityBuild buildName={job.build_job}/>,
                  relUrl: 'build'
                }, {
                  title: 'Statuses',
                  component: <Statuses
                    project={job.project}
                    resource="jobs"
                    id={job.id}
                  />,
                  relUrl: 'statuses'
                }, {
                  title: 'Instructions',
                  component: <JobInstructions id={job.id}/>,
                  relUrl: 'instructions'
                }
              ]}
            />
          </div>
        </div>
      </div>
    );
  }
}
