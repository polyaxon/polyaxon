import { connect, Dispatch } from 'react-redux';
import { withRouter } from 'react-router-dom';
import * as _ from 'lodash';

import { AppState } from '../constants/types';

import ExperimentJobDetail from '../components/experimentJobDetail';
import * as actions from '../actions/experimentJob';
import { getExperimentJobUniqueName } from '../constants/utils';

export function mapStateToProps(state: AppState, params: any)  {
  let jobUniqueName = getExperimentJobUniqueName(
    params.match.params.user,
    params.match.params.projectName,
    params.match.params.experimentId,
    params.match.params.jobId);
  return _.includes(state.jobs.uniqueNames, jobUniqueName) ?
      {job: state.jobs.byUniqueNames[jobUniqueName]} :
      {job: null};
}

export interface DispatchProps {
  onDelete?: () => any;
  fetchData?: () => any;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ExperimentJobAction>, params: any): DispatchProps {
  return {
    fetchData: () => dispatch(
      actions.fetchExperimentJob(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.experimentId,
        params.match.params.jobId))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ExperimentJobDetail));
