import * as _ from 'lodash';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import { AppState } from '../constants/types';

import * as actions from '../actions/experimentJob';
import ExperimentJobDetail from '../components/experimentJobs/experimentJobDetail';
import { getExperimentJobUniqueName } from '../constants/utils';

export function mapStateToProps(state: AppState, params: any) {
  const jobUniqueName = getExperimentJobUniqueName(
    params.match.params.user,
    params.match.params.projectName,
    params.match.params.experimentId,
    params.match.params.jobId);
  return _.includes(state.experimentJobs.uniqueNames, jobUniqueName) ?
    {job: state.experimentJobs.byUniqueNames[jobUniqueName]} :
    {job: null};
}

export interface DispatchProps {
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
