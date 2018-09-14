import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../../actions/job';
import {
  getJobUrl,
  getProjectUrl,
  getUserUrl,
  splitUniqueName,
} from '../../constants/utils';
import EntityBuild from '../../containers/entityBuild';
import Logs from '../../containers/logs';
import Statuses from '../../containers/statuses';
import { ActionInterface } from '../../interfaces/actions';
import { BookmarkInterface } from '../../interfaces/bookmarks';
import { JobModel } from '../../models/job';
import { getBookmark } from '../../utils/bookmarks';
import Breadcrumb from '../breadcrumb';
import { EmptyList } from '../empty/emptyList';
import JobInstructions from '../instructions/jobInstructions';
import JobOverview from './jobOverview';
import LinkedTab from '../linkedTab';
import YamlText from '../yamlText';

export interface Props {
  job: JobModel;
  onDelete: () => actions.JobAction;
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

    const action: ActionInterface = {
      last_status: this.props.job.last_status,
      onDelete: this.props.onDelete,
      onStop: this.props.onStop

    };

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
              actions={action}
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
