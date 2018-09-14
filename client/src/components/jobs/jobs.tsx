import * as React from 'react';

import * as actions from '../../actions/job';
import * as search_actions from '../../actions/search';
import { JOB_FILTER_OPTIONS } from '../../constants/filtering';
import { DEFAULT_SORT_OPTIONS } from '../../constants/sorting';
import { JobModel } from '../../models/job';
import { SearchModel } from '../../models/search';
import { EmptyBookmarks } from '../empty/emptyBookmarks';
import { EmptyList } from '../empty/emptyList';
import { DEFAULT_FILTERS } from '../filters/constants';
import PaginatedTable from '../paginatedTable';
import Job from './job';
import JobHeader from './jobHeader';

export interface Props {
  isCurrentUser: boolean;
  jobs: JobModel[];
  count: number;
  useFilters: boolean;
  showBookmarks: boolean;
  bookmarks: boolean;
  onCreate: (job: JobModel) => actions.JobAction;
  onUpdate: (job: JobModel) => actions.JobAction;
  onDelete: (jobName: string) => actions.JobAction;
  onStop: (jobName: string) => actions.JobAction;
  bookmark: (jobName: string) => actions.JobAction;
  unbookmark: (jobName: string) => actions.JobAction;
  fetchData: (offset?: number, query?: string, sort?: string) => actions.JobAction;
  fetchSearches?: () => search_actions.SearchAction;
  createSearch?: (data: SearchModel) => search_actions.SearchAction;
  deleteSearch?: (searchId: number) => search_actions.SearchAction;
}

export default class Jobs extends React.Component<Props, {}> {
  public render() {
    const filters = this.props.useFilters ? DEFAULT_FILTERS : false;
    const jobs = this.props.jobs;
    const listJobs = () => {
      return (
        <table className="table table-hover table-responsive">
          <tbody>
          {JobHeader()}
          {jobs.map(
            (job: JobModel) =>
              <Job
                key={job.unique_name}
                job={job}
                onDelete={() => this.props.onDelete(job.unique_name)}
                onStop={() => this.props.onStop(job.unique_name)}
                showBookmarks={this.props.showBookmarks}
                bookmark={() => this.props.bookmark(job.unique_name)}
                unbookmark={() => this.props.unbookmark(job.unique_name)}
              />)}
          </tbody>
        </table>
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
        sortOptions={DEFAULT_SORT_OPTIONS}
        filterOptions={JOB_FILTER_OPTIONS}
        fetchSearches={this.props.fetchSearches}
        createSearch={this.props.createSearch}
        deleteSearch={this.props.deleteSearch}
      />
    );
  }
}
