import * as React from 'react';
import * as _ from 'lodash';

import * as actions from '../actions/job';
import Job from './job';
import { JobModel } from '../models/job';
import { DEFAULT_FILTERS } from './filters/constants';
import PaginatedList from './paginatedList';
import { EmptyList } from './emptyList';
import JobHeader from './jobHeader';

export interface Props {
  jobs: JobModel[];
  count: number;
  onCreate: (job: JobModel) => actions.JobAction;
  onUpdate: (job: JobModel) => actions.JobAction;
  onDelete: (job: JobModel) => actions.JobAction;
  fetchData: (offset?: number, query?: string, sort?: string) => actions.JobAction;
}

export default class Jobs extends React.Component<Props, Object> {
  public render() {
    const jobs = this.props.jobs;
    const listJobs = () => {
      return (
        <ul>
          {jobs.filter(
            (xp: JobModel) => _.isNil(xp.deleted) || !xp.deleted
          ).map(
            (job: JobModel) =>
              <li className="list-item" key={job.unique_name}>
                <Job job={job} onDelete={() => this.props.onDelete(job)}/>
              </li>)}
        </ul>
      );
    };
    return (
      <PaginatedList
        count={this.props.count}
        componentList={listJobs()}
        componentHeader={JobHeader()}
        componentEmpty={EmptyList(false, 'job', 'job')}
        filters={DEFAULT_FILTERS}
        fetchData={this.props.fetchData}
      />
    );
  }
}
