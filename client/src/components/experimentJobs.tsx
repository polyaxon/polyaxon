import * as React from 'react';
import * as _ from 'lodash';

import * as actions from '../actions/experimentJob';
import ExperimentJob from './experimentJob';
import { ExperimentJobModel } from '../models/experimentJob';
import PaginatedList from '../components/paginatedList';
import { EmptyList } from './emptyList';
import JobHeader from './jobHeader';

export interface Props {
  jobs: ExperimentJobModel[];
  count: number;
  onCreate: (job: ExperimentJobModel) => actions.ExperimentJobAction;
  onUpdate: (job: ExperimentJobModel) => actions.ExperimentJobAction;
  onDelete: (job: ExperimentJobModel) => actions.ExperimentJobAction;
  fetchData: (currentPage: number) => actions.ExperimentJobAction;
}

export default class ExperimentJobs extends React.Component<Props, Object> {
  public render() {
    const jobs = this.props.jobs;
    const listExperimentJobs = () => {
      return (
        <ul>
          {jobs.filter(
            (xp: ExperimentJobModel) => _.isNil(xp.deleted) || !xp.deleted
          ).map(
            (experimentJob: ExperimentJobModel) =>
              <li className="list-item" key={experimentJob.unique_name}>
                <ExperimentJob
                  experimentJob={experimentJob}
                  onDelete={() => this.props.onDelete(experimentJob)}
                />
              </li>)}
        </ul>
      );
    };
    return (
      <PaginatedList
        count={this.props.count}
        componentList={listExperimentJobs()}
        componentHeader={JobHeader()}
        componentEmpty={EmptyList(false, 'job', 'job')}
        fetchData={this.props.fetchData}
      />
    );
  }
}
