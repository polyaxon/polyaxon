import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import * as actions from '../../actions/experimentJobs';
import ExperimentJobs from '../../components/experimentJobs/experimentJobs';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { getErrorsGlobal } from '../../utils/errors';
import { getLastFetchedExperimentJobs } from '../../utils/states';

export function mapStateToProps(state: AppState, props: any) {
  const results = getLastFetchedExperimentJobs(state.experimentJobs);

  const isLoading = isTrue(state.loadingIndicators.experimentJobs.global.fetch);
  return {
    jobs: results.jobs,
    count: results.count,
    isLoading,
    errors: getErrorsGlobal(state.alerts.experimentJobs.global, isLoading, ACTIONS.FETCH),
  };
}

export interface DispatchProps {
  fetchData?: (offset?: number, query?: string, sort?: string) => actions.ExperimentJobAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ExperimentJobAction>, props: any): DispatchProps {
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
        props.experiment.project,
        props.experiment.id,
        filters));
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(ExperimentJobs);
