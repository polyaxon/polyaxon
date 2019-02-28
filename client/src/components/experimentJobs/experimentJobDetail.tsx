import * as _ from 'lodash';
import * as React from 'react';

import { ExperimentJobModel } from '../../models/experimentJob';
import { EmptyList } from '../empty/emptyList';

import {
  getExperimentJobUrl, getExperimentUrl,
  getProjectUrl,
  getUserUrl,
  splitUniqueName,
} from '../../constants/utils';
import Logs from '../../containers/logs';
import Statuses from '../../containers/statuses';
import Breadcrumb from '../breadcrumb';
import ExperimentJobInstructions from '../instructions/experimentJobInstructions';
import LinkedTab from '../linkedTab';
import ExperimentJobOverview from './experimentJobOverview';

export interface Props {
  job: ExperimentJobModel;
  fetchData: () => any;
}

export default class JobDetail extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const job = this.props.job;
    if (_.isNil(job)) {
      return EmptyList(false, 'experiment job', 'job');
    }
    const values = splitUniqueName(job.unique_name);
    const user = values[0];
    const project = values[1];
    const projectUniqueName = `${user}.${project}`;
    const projectUrl = getProjectUrl(user, project);
    const experimentUrl = getExperimentUrl(user, project, job.experiment);
    const jobUrl = getExperimentJobUrl(user, project, job.experiment, job.id);
    const breadcrumbLinks = [
      {name: user, value: getUserUrl(user)},
      {name: project, value: projectUrl},
      {name: `Experiment ${job.experiment}`, value: experimentUrl},
      {name: `Jobs`, value: `${experimentUrl}#jobs`},
      {name: `Job ${job.id}`}];
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <Breadcrumb
              icon="fa-tasks"
              links={breadcrumbLinks}
            />
            <LinkedTab
              baseUrl={jobUrl}
              tabs={[
                {
                  title: 'Overview',
                  component: <ExperimentJobOverview
                    job={job}
                    onFetch={this.props.fetchData}
                  />,
                  relUrl: ''
                }, {
                  title: 'Logs',
                  component: <Logs
                    fetchData={() => null}
                    logs={''}
                    project={projectUniqueName}
                    resource="experiments"
                    id={job.experiment}
                    subResource="jobs"
                    sid={job.id}
                  />,
                  relUrl: 'logs'
                }, {
                  title: 'Statuses',
                  component: <Statuses
                    project={projectUniqueName}
                    resource="experiments"
                    id={job.experiment}
                    subResource="jobs"
                    sid={job.id}
                  />,
                  relUrl: 'statuses'
                }, {
                  title: 'Instructions',
                  component: <ExperimentJobInstructions id={job.id}/>,
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
