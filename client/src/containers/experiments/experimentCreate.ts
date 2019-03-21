import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../actions/experiment';
import * as modalActions from '../../actions/modal';
import ExperimentCreate from '../../components/experiments/experimentCreate';
import { AppState } from '../../constants/types';
import { ExperimentModel } from '../../models/experiment';

export function mapStateToProps(state: AppState, params: any) {
  return {
    user: params.match.params.user,
    projectName: params.match.params.projectName,
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
        experiment)),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ExperimentCreate));
