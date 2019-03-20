import { connect } from 'react-redux';
import { Dispatch } from 'redux';

import * as modalActions from '../../actions/modal';
import * as actions from '../../actions/project';
import ProjectCreate from '../../components/projects/projectCreate';
import { AppState } from '../../constants/types';
import { ProjectModel } from '../../models/project';

interface OwnProps {
  user: string;
  endpointList?: string;
  showBookmarks?: boolean;
  showDeleted?: boolean;
  fetchData?: () => actions.ProjectAction;
}

export function mapStateToProps(state: AppState, ownProps: OwnProps) {
  return {
    isCurrentUser: state.auth.user === ownProps.user,
    user: ownProps.user,
  };
}

export interface DispatchProps {
  onCreate: (project: ProjectModel) => actions.ProjectAction;
}

export function mapDispatchToProps(
  dispatch: Dispatch<actions.ProjectAction | modalActions.ModalAction>, ownProps: OwnProps): DispatchProps {
  return {
    onCreate: (project: ProjectModel) => dispatch(actions.createProject(ownProps.user, project)),
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(ProjectCreate);
