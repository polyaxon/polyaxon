import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../actions/job';
import { JobModel } from '../models/job';
import { EmptyBookmarks } from './empty/emptyBookmarks';
import { EmptyList } from './empty/emptyList';
import { DEFAULT_FILTERS } from './filters/constants';
import Job from './job';
import JobHeader from './jobHeader';
import PaginatedList from './paginatedList';

export interface Props {
  isCurrentUser: boolean;
  jobs: JobModel[];
  count: number;
  useFilters: boolean;
  bookmarks: boolean;
  onCreate: (job: JobModel) => actions.JobAction;
  onUpdate: (job: JobModel) => actions.JobAction;
  onDelete: (job: JobModel) => actions.JobAction;
  fetchData: (offset?: number, query?: string, sort?: string) => actions.JobAction;
}

export default class Jobs extends React.Component<Props, Object> {
  public render() {
    const filters = this.props.useFilters ? DEFAULT_FILTERS : false;
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

    const empty = this.props.bookmarks ?
      EmptyBookmarks(
        this.props.isCurrentUser,
        'job',
        'job')
      : EmptyList(
        this.props.isCurrentUser,
        'job',
        'job',
        'polyaxon run --help');

    return (
      <PaginatedList
        count={this.props.count}
        componentList={listJobs()}
        componentHeader={JobHeader()}
        componentEmpty={empty}
        filters={filters}
        fetchData={this.props.fetchData}
      />
    );
  }
}
