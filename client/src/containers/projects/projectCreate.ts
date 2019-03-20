import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import * as modalActions from '../../actions/modal';
import * as actions from '../../actions/project';
import ProjectCreate from '../../components/projects/projectCreate';
import { AppState } from '../../constants/types';
import { ProjectModel } from '../../models/project';

export function mapStateToProps(state: AppState, ownProps: {}) {
  return {
    user: state.auth.user,
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
