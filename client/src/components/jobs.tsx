import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../actions/job';
import { JobModel } from '../models/job';
import { EmptyBookmarks } from './empty/emptyBookmarks';
import { EmptyList } from './empty/emptyList';
import { DEFAULT_FILTERS } from './filters/constants';
import Job from './job';
import JobHeader from './jobHeader';
import PaginatedTable from './paginatedTable';

export interface Props {
  isCurrentUser: boolean;
  jobs: JobModel[];
  count: number;
  useFilters: boolean;
  bookmarks: boolean;
  onCreate: (job: JobModel) => actions.JobAction;
  onUpdate: (job: JobModel) => actions.JobAction;
  onDelete: (jobName: string) => actions.JobAction;
  onStop: (jobName: string) => actions.JobAction;
  fetchData: (offset?: number, query?: string, sort?: string) => actions.JobAction;
}

export default class Jobs extends React.Component<Props, Object> {
  public render() {
    const filters = this.props.useFilters ? DEFAULT_FILTERS : false;
    const jobs = this.props.jobs;
    const listJobs = () => {
      return (
        <tbody>
        {JobHeader()}
        {jobs.map(
          (job: JobModel) =>
            <Job
              key={job.unique_name}
              job={job}
              onDelete={() => this.props.onDelete(job.unique_name)}
              onStop={() => this.props.onStop(job.unique_name)}
            />)}
        </tbody>
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
      <PaginatedTable
        count={this.props.count}
        componentList={listJobs()}
        componentEmpty={empty}
        filters={filters}
        fetchData={this.props.fetchData}
      />
    );
  }
}
