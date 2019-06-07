import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../actions/projects';
import User from '../components/user';
import { AppState } from '../constants/types';
import { ProjectModel } from '../models/project';

interface Props extends RouteComponentProps<any> {}

export function mapStateToProps(state: AppState, props: Props) {
  return {user: props.match.params.user};
}

export interface DispatchProps {
  createProject: (project: ProjectModel) => actions.ProjectAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ProjectAction>, props: Props): DispatchProps {
  return {
    createProject: (project: ProjectModel) => dispatch(actions.createProject(project))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(User));
