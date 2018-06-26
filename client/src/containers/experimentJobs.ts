import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import { getExperimentIndexName } from '../constants/utils';
import { AppState } from '../constants/types';
import ExperimentJobs from '../components/experimentJobs';
import { ExperimentJobModel } from '../models/experimentJob';

import * as actions from '../actions/experimentJob';

export function mapStateToProps(state: AppState, params: any) {
  let useFilter = () => {
    let experimentName = getExperimentIndexName(params.experiment.unique_name);
    let jobs: ExperimentJobModel[] = [];
    let experiment = state.experiments.byUniqueNames[experimentName];
    let jobNames = experiment.jobs;
    jobNames.forEach(
      function (job: string, idx: number) {
        jobs.push(state.experimentJobs.byUniqueNames[job]);
      });
    return {jobs: jobs, count: experiment.num_jobs};
  };

  let useLastFetched = () => {
    let jobNames = state.experimentJobs.lastFetched.names;
    let count = state.experimentJobs.lastFetched.count;
    let jobs: ExperimentJobModel[] = [];
    jobNames.forEach(
      function (job: string, idx: number) {
        jobs.push(state.experimentJobs.byUniqueNames[job]);
      });
    return {jobs: jobs, count: count};
  };
  let results = useLastFetched();

  return {jobs: results.jobs, count: results.count};
}

export interface DispatchProps {
  onCreate?: (job: ExperimentJobModel) => actions.ExperimentJobAction;
  onDelete?: (job: ExperimentJobModel) => actions.ExperimentJobAction;
  onUpdate?: (job: ExperimentJobModel) => actions.ExperimentJobAction;
  fetchData?: (offset?: number, query?: string, sort?: string) => actions.ExperimentJobAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ExperimentJobAction>, params: any): DispatchProps {
  return {
    onCreate: (job: ExperimentJobModel) => dispatch(actions.createExperimentJobActionCreator(job)),
    onDelete: (job: ExperimentJobModel) => dispatch(actions.deleteExperimentJobActionCreator(job)),
    onUpdate: (job: ExperimentJobModel) => dispatch(actions.updateExperimentJobActionCreator(job)),
    fetchData: (offset?: number, query?: string, sort?: string) => {
      let filters: { [key: string]: number | boolean | string } = {};
      if (query) {
        filters.query = query;
      }
      if (sort) {
        filters.sort = sort;
      }
      if (offset) {
        filters.offset = offset;
      }
      return dispatch(actions.fetchExperimentJobs(
        params.experiment.project,
        params.experiment.id,
        filters));
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(ExperimentJobs);
