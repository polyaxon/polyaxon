import * as React from 'react';

import * as actions from '../../actions/experimentJobs';
import { ExperimentJobModel } from '../../models/experimentJob';
import { isLive } from '../../utils/isLive';
import { EmptyList } from '../empty/emptyList';
import PaginatedList from '../tables/paginatedList';
import ExperimentJob from './experimentJob';
import ExperimentJobHeader from './experimentJobHeader';

export interface Props {
  jobs: ExperimentJobModel[];
  count: number;
  fetchData: (offset?: number, query?: string, sort?: string) => actions.ExperimentJobAction;
  isLoading: boolean;
  errors: any;
}

export default class ExperimentJobs extends React.Component<Props, {}> {
  public render() {
    const jobs = this.props.jobs;
    const listExperimentJobs = () => {
      return (
        <ul>
          {jobs.filter(
            (xp: ExperimentJobModel) => isLive(xp)
          ).map(
            (experimentJob: ExperimentJobModel) =>
              <li className="list-item" key={experimentJob.unique_name}>
                <ExperimentJob experimentJob={experimentJob}/>
              </li>)}
        </ul>
      );
    };
    return (
      <PaginatedList
        isLoading={this.props.isLoading}
        errors={this.props.errors}
        count={this.props.count}
        componentList={listExperimentJobs()}
        componentHeader={ExperimentJobHeader()}
        componentEmpty={EmptyList(false, 'job', 'job')}
        filters={false}
        fetchData={this.props.fetchData}
      />
    );
  }
}
