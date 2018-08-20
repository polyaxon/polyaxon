import * as _ from 'lodash';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../actions/experiment';
import ExperimentDetail from '../components/experimentDetail';
import { AppState } from '../constants/types';
import { getExperimentUniqueName } from '../constants/utils';

export function mapStateToProps(state: AppState, params: any)  {
  const experimentUniqueName = getExperimentUniqueName(
    params.match.params.user,
    params.match.params.projectName,
    params.match.params.experimentId);
  return _.includes(state.experiments.uniqueNames, experimentUniqueName) ?
    {experiment: state.experiments.byUniqueNames[experimentUniqueName]} :
    {experiment: null};
}

export interface DispatchProps {
  onDelete?: () => any;
  fetchData?: () => any;
  bookmark: () => any;
  unbookmark: () => any;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ExperimentAction>, params: any): DispatchProps {
  return {
    fetchData: () => dispatch(
      actions.fetchExperiment(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.experimentId)),
    bookmark: () => dispatch(
      actions.bookmark(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.experimentId)),
    unbookmark: () => dispatch(
      actions.unbookmark(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.experimentId))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ExperimentDetail));
