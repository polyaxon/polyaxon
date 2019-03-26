import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import * as modalActions from '../../actions/modal';
import * as actions from '../../actions/projects';
import ProjectCreate from '../../components/projects/projectCreate';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { ProjectModel } from '../../models/project';
import { getErrorsGlobal } from '../../utils/errors';

export function mapStateToProps(state: AppState, ownProps: {}) {
  const isLoading = isTrue(state.loadingIndicators.projects.global.create);
  return {
    user: state.auth.user,
    isLoading,
    errors: getErrorsGlobal(state.errors.projects.global, isLoading, ACTIONS.CREATE),
  };
}

export interface DispatchProps {
  onCreate: (project: ProjectModel) => actions.ProjectAction;
}

export function mapDispatchToProps(
  dispatch: Dispatch<actions.ProjectAction | modalActions.ModalAction>, ownProps: {}): DispatchProps {
  return {
    onCreate: (project: ProjectModel) => dispatch(actions.createProject(project, true)),
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(ProjectCreate);
