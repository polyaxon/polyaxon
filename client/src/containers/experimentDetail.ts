import { connect, Dispatch } from 'react-redux';
import { withRouter } from 'react-router-dom';
import * as _ from 'lodash';

import { AppState } from '../constants/types';
import ExperimentDetail from '../components/experimentDetail';
import * as actions from '../actions/experiment';
import { getExperimentUniqueName } from '../constants/utils';

export function mapStateToProps(state: AppState, params: any)  {
  let experimentUniqueName = getExperimentUniqueName(
    params.match.params.user,
    params.match.params.projectName,
    params.match.params.experimentSequence);
  return _.includes(state.experiments.uniqueNames, experimentUniqueName) ?
    {experiment: state.experiments.byUniqueNames[experimentUniqueName]} :
    {experiment: null};
}

export interface DispatchProps {
  onDelete?: () => any;
  fetchData?: () => any;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ExperimentAction>, params: any): DispatchProps {
  return {
    onDelete: () => dispatch(() => undefined),
    fetchData: () => dispatch(
      actions.fetchExperiment(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.experimentSequence))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ExperimentDetail));
