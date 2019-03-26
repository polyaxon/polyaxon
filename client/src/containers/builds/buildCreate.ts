import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../actions/builds';
import * as modalActions from '../../actions/modal';
import BuildCreate from '../../components/builds/buildCreate';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { BuildModel } from '../../models/build';
import { getErrorsGlobal } from '../../utils/errors';

export function mapStateToProps(state: AppState, params: any) {
  const isLoading = isTrue(state.loadingIndicators.builds.global.create);
  return {
    user: params.match.params.user,
    projectName: params.match.params.projectName,
    isLoading,
    errors: getErrorsGlobal(state.alerts.builds.global, isLoading, ACTIONS.CREATE),
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
