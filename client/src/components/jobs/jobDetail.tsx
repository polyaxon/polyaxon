import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../../actions/job';
import { isDone } from '../../constants/statuses';
import {
  getJobUrl,
  getProjectUrl,
  getUserUrl,
  splitUniqueName,
} from '../../constants/utils';
import EntityBuild from '../../containers/entityBuild';
import Logs from '../../containers/logs';
import Outputs from '../../containers/outputs';
import Statuses from '../../containers/statuses';
import { BookmarkInterface } from '../../interfaces/bookmarks';
import { JobModel } from '../../models/job';
import { getBookmark } from '../../utils/bookmarks';
import Breadcrumb from '../breadcrumb';
import { EmptyList } from '../empty/emptyList';
import JobInstructions from '../instructions/jobInstructions';
import LinkedTab from '../linkedTab';
import YamlText from '../yamlText';
import JobActions from './jobActions';
import JobOverview from './jobOverview';

export interface Props {
  job: JobModel;
  onUpdate: (updateDict: { [key: string]: any }) => actions.JobAction;
  onDelete: () => actions.JobAction;
  onArchive: () => actions.JobAction;
  onRestore: () => actions.JobAction;
  onStop: () => actions.JobAction;
  fetchData: () => actions.JobAction;
  bookmark: () => actions.JobAction;
  unbookmark: () => actions.JobAction;
}

export default class JobDetail extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const job = this.props.job;
    if (_.isNil(job)) {
      return EmptyList(false, 'job', 'job');
    }

    const bookmark: BookmarkInterface = getBookmark(
      this.props.job.bookmarked, this.props.bookmark, this.props.unbookmark);
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
              actions={
                <JobActions
                  onDelete={this.props.onDelete}
                  onStop={this.props.onStop}
                  onArchive={job.deleted ? undefined : this.props.onArchive}
                  onRestore={job.deleted ? this.props.onRestore : undefined}
                  isRunning={!isDone(this.props.job.last_status)}
                  pullRight={true}
                />
              }
            />
            <LinkedTab
              baseUrl={jobUrl}
              tabs={[
                {
                  title: 'Overview',
                  component: <JobOverview
                    job={job}
                    onUpdate={this.props.onUpdate}
                    onFetch={this.props.fetchData}
                  />,
                  relUrl: ''
                }, {
                  title: 'Logs',
                  component: <Logs
                    fetchData={() => null}
                    logs={''}
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
                  title: 'Outputs',
                  component: <Outputs
                    user={job.user}
                    project={job.project}
                    resource="jobs"
                    id={job.id}
                  />,
                  relUrl: 'outputs'
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
