import * as _ from 'lodash';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../actions/experiment';
import * as codeRefActions from '../actions/codeReference';
import ExperimentDetail from '../components/experimentDetail';
import { AppState } from '../constants/types';
import { getExperimentUniqueName } from '../constants/utils';

export function mapStateToProps(state: AppState, params: any) {
  const experimentUniqueName = getExperimentUniqueName(
    params.match.params.user,
    params.match.params.projectName,
    params.match.params.experimentId);
  return _.includes(state.experiments.uniqueNames, experimentUniqueName) ?
    {experiment: state.experiments.byUniqueNames[experimentUniqueName]} :
    {experiment: null};
}

export interface DispatchProps {
  fetchData?: () => actions.ExperimentAction;
  onDelete: () => actions.ExperimentAction;
  onStop: () => actions.ExperimentAction;
  bookmark: () => actions.ExperimentAction;
  unbookmark: () => actions.ExperimentAction;
  fetchCodeReference: () => codeRefActions.CodeReferenceAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ExperimentAction>, params: any): DispatchProps {
  return {
    fetchData: () => dispatch(
      actions.fetchExperiment(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.experimentId)),
    onDelete: () => dispatch(
      actions.deleteExperiment(
        getExperimentUniqueName(
          params.match.params.user,
          params.match.params.projectName,
          params.match.params.experimentId),
        true)),
    onStop: () => dispatch(
      actions.stopExperiment(
        getExperimentUniqueName(
          params.match.params.user,
          params.match.params.projectName,
          params.match.params.experimentId))),
    bookmark: () => dispatch(
      actions.bookmark(getExperimentUniqueName(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.experimentId))),
    unbookmark: () => dispatch(
      actions.unbookmark(getExperimentUniqueName(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.experimentId))),
    fetchCodeReference: () => dispatch(
      actions.fetchExperimentCodeReference(getExperimentUniqueName(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.experimentId)))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ExperimentDetail));
