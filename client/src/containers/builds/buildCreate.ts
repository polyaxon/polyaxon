import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../actions/builds';
import * as modalActions from '../../actions/modal';
import BuildCreate from '../../components/builds/buildCreate';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { BuildModel } from '../../models/build';

export function mapStateToProps(state: AppState, params: any) {
  return {
    user: params.match.params.user,
    projectName: params.match.params.projectName,
    isLoading: isTrue(state.loadingIndicators.builds.global.create),
    errors: state.errors.builds.global.create,
  };
}

export interface DispatchProps {
  onCreate: (build: BuildModel) => actions.BuildAction;
}

export function mapDispatchToProps(
  dispatch: Dispatch<actions.BuildAction | modalActions.ModalAction>, params: any): DispatchProps {
  return {
    onCreate: (build: BuildModel) => dispatch(
      actions.createBuild(
        params.match.params.user,
        params.match.params.projectName,
        build,
        true)),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(BuildCreate));
