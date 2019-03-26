import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../actions/projects';
import * as modalActions from '../../actions/modal';
import NotebookCreate from '../../components/notebooks/notebookCreate';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { NotebookModel } from '../../models/notebook';

export function mapStateToProps(state: AppState, params: any) {
  return {
    user: params.match.params.user,
    projectName: params.match.params.projectName,
    isLoading: isTrue(state.loadingIndicators.notebooks.global.create),
    errors: state.errors.notebooks.global.create,
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
