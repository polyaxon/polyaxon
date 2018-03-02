import * as React from 'react';
import * as _ from 'lodash';

import * as actions from '../actions/job';
import Job from './job';
import { JobModel } from '../models/job';
import PaginatedList from '../components/paginatedList';
import { noObjectListComponent } from '../constants/templates';

export interface Props {
  jobs: JobModel[];
  count: number;
  onCreate: (job: JobModel) => actions.JobAction;
  onUpdate: (job: JobModel) => actions.JobAction;
  onDelete: (job: JobModel) => actions.JobAction;
  fetchData: (currentPage: number) => actions.JobAction;
}

export default class Jobs extends React.Component<Props, Object> {
  public render() {
    const jobs = this.props.jobs;
    const listJobs = () => {
      if (jobs.length === 0) {
        return noObjectListComponent(false, 'job', 'job');
      }
      return (
        <div className="col-md-12">
          <ul>
            {jobs.filter(
              (xp: JobModel) => _.isNil(xp.deleted) || !xp.deleted
            ).map(
              (job: JobModel) =>
                <li className="list-item" key={job.unique_name}>
                  <Job job={job} onDelete={() => this.props.onDelete(job)}/>
                </li>)}
          </ul>
        </div>
      );
    };
    return (
      <PaginatedList
        count={this.props.count}
        componentList={listJobs()}
        fetchData={this.props.fetchData}
      />
    );
  }
}
