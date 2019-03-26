import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../actions/experiments';
import * as modalActions from '../../actions/modal';
import ExperimentCreate from '../../components/experiments/experimentCreate';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { ExperimentModel } from '../../models/experiment';
import { getErrorsGlobal } from '../../utils/errors';

export function mapStateToProps(state: AppState, params: any) {
  const isLoading = isTrue(state.loadingIndicators.experiments.global.create);
  return {
    user: params.match.params.user,
    projectName: params.match.params.projectName,
    isLoading,
    errors: getErrorsGlobal(state.errors.experiments.global, isLoading, ACTIONS.CREATE),
  };
}

export interface DispatchProps {
  onCreate: (experiment: ExperimentModel) => actions.ExperimentAction;
}

export function mapDispatchToProps(
  dispatch: Dispatch<actions.ExperimentAction | modalActions.ModalAction>, params: any): DispatchProps {
  return {
    onCreate: (experiment: ExperimentModel) => dispatch(
      actions.createExperiment(
        params.match.params.user,
        params.match.params.projectName,
        experiment,
        true)),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ExperimentCreate));
