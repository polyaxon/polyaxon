import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import * as actions from '../../actions/experimentJobs';
import ExperimentJobs from '../../components/experimentJobs/experimentJobs';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { getExperimentIndexName, isTrue } from '../../constants/utils';
import { ExperimentJobModel } from '../../models/experimentJob';
import { getErrorsGlobal } from '../../utils/errors';

export function mapStateToProps(state: AppState, params: any) {
  const useFilter = () => {
    const experimentName = getExperimentIndexName(params.experiment.unique_name);
    const jobs: ExperimentJobModel[] = [];
    const experiment = state.experiments.byUniqueNames[experimentName];
    const jobNames = experiment.jobs;
    jobNames.forEach(
      (job: string, idx: number) => {
        jobs.push(state.experimentJobs.byUniqueNames[job]);
      });
    return {jobs, count: experiment.num_jobs};
  };

  const useLastFetched = () => {
    const jobNames = state.experimentJobs.lastFetched.names;
    const count = state.experimentJobs.lastFetched.count;
    const jobs: ExperimentJobModel[] = [];
    jobNames.forEach(
      function (job: string, idx: number) {
        jobs.push(state.experimentJobs.byUniqueNames[job]);
      });
    return {jobs, count};
  };
  const results = useLastFetched();

  const isLoading = isTrue(state.loadingIndicators.experimentJobs.global.fetch);
  return {
    jobs: results.jobs,
    count: results.count,
    isLoading,
    errors: getErrorsGlobal(state.errors.experimentJobs.global, isLoading, ACTIONS.FETCH),
  };
}

export interface DispatchProps {
  fetchData?: (offset?: number, query?: string, sort?: string) => actions.ExperimentJobAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ExperimentJobAction>, params: any): DispatchProps {
  return {
    fetchData: (offset?: number, query?: string, sort?: string) => {
      const filters: { [key: string]: number | boolean | string } = {};
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
