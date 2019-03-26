import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as modalActions from '../../actions/modal';
import * as actions from '../../actions/projects';
import NotebookCreate from '../../components/notebooks/notebookCreate';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { NotebookModel } from '../../models/notebook';
import { getErrorsGlobal } from '../../utils/errors';

export function mapStateToProps(state: AppState, params: any) {
  const isLoading = isTrue(state.loadingIndicators.notebooks.global.create);
  return {
    user: params.match.params.user,
    projectName: params.match.params.projectName,
    isLoading,
    errors: getErrorsGlobal(state.alerts.notebooks.global, isLoading, ACTIONS.CREATE),
  };
}

export interface DispatchProps {
  onCreate: (notebook: NotebookModel) => actions.ProjectAction;
}

export function mapDispatchToProps(
  dispatch: Dispatch<actions.ProjectAction | modalActions.ModalAction>, params: any): DispatchProps {
  return {
    onCreate: (notebook: NotebookModel) => dispatch(
      actions.startNotebook(
        params.match.params.user,
        params.match.params.projectName,
        notebook,
        true)),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(NotebookCreate));
