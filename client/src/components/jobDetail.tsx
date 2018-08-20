import * as _ from 'lodash';
import * as React from 'react';

import { Bookmark } from '../constants/bookmarks';
import {
  getJobUrl,
  getProjectUrl,
  getUserUrl,
  isTrue,
  splitUniqueName,
} from '../constants/utils';
import EntityBuild from '../containers/EntityBuild';
import Logs from '../containers/logs';
import Statuses from '../containers/statuses';
import { JobModel } from '../models/job';
import Breadcrumb from './breadcrumb';
import { EmptyList } from './empty/emptyList';
import JobInstructions from './instructions/jobInstructions';
import JobOverview from './jobOverview';
import LinkedTab from './linkedTab';
import YamlText from './yamlText';

export interface Props {
  job: JobModel;
  onDelete: () => any;
  fetchData: () => any;
  bookmark: () => any;
  unbookmark: () => any;
}

export default class JobDetail extends React.Component<Props, Object> {
  public componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const job = this.props.job;
    if (_.isNil(job)) {
      return EmptyList(false, 'job', 'job');
    }

    const bookmark: Bookmark = {
      active: isTrue(this.props.job.bookmarked),
      callback: isTrue(this.props.job.bookmarked) ? this.props.unbookmark : this.props.bookmark
    };
    const values = splitUniqueName(job.project);
    const jobUrl = getJobUrl(values[0], values[1], this.props.job.id);
    const projectUrl = getProjectUrl(values[0], values[1]);
    const breadcrumbLinks = [
      {name: values[0], value: getUserUrl(values[0])},
      {name: values[1], value: projectUrl},
      {name: 'Jobs', value: `${projectUrl}#jobs`},
      {name: `Job ${job.id}`}];
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <Breadcrumb
              icon="fa-tasks"
              links={breadcrumbLinks}
              bookmark={bookmark}
            />
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
                  title: 'Config',
                  component: <YamlText title="Config" config={job.config}/>,
                  relUrl: 'config'
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
