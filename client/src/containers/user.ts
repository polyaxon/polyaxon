import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../actions/project';
import User from '../components/user';
import { AppState } from '../constants/types';
import { ProjectModel } from '../models/project';

export function mapStateToProps(state: AppState, params: any) {
  return {user: params.match.params.user};
}

export interface DispatchProps {
  createProject: (project: ProjectModel) => actions.ProjectAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ProjectAction>, params: any): DispatchProps {
  return {
    createProject: (project: ProjectModel) => dispatch(actions.createProject(project))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(User));
