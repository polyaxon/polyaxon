import * as _ from 'lodash';
import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as buildsActions from '../../actions/builds';
import * as projectsActions from '../../actions/projects';
import BuildCreate from '../../components/builds/buildCreate';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { BuildModel } from '../../models/build';
import { getErrorsGlobal } from '../../utils/errors';
import { getLastFetchedProjects } from '../../utils/states';

interface Props extends RouteComponentProps<any> {}

export function mapStateToProps(state: AppState, props: Props) {
  const isLoading = isTrue(state.loadingIndicators.builds.global.create);
  const isProjectEntity = _.isNil(props.match.params.user);
  const projects = isProjectEntity ? getLastFetchedProjects(state.projects).projects : [];
  return {
    user: props.match.params.user || state.auth.user,
    projectName: props.match.params.projectName,
    isProjectEntity,
    isLoading,
    projects,
    errors: getErrorsGlobal(state.alerts.builds.global, isLoading, ACTIONS.CREATE),
  };
}

export interface DispatchProps {
  onCreate: (build: BuildModel) => buildsActions.BuildAction;
  fetchProjects: (user: string) => projectsActions.ProjectAction;
}

export function mapDispatchToProps(
  dispatch: Dispatch<buildsActions.BuildAction>, props: Props): DispatchProps {
  return {
    onCreate: (build: BuildModel, user?: string, projectName?: string) => dispatch(
      buildsActions.createBuild(
        user || props.match.params.user,
        projectName || props.match.params.projectName,
        build,
        true)),
    fetchProjects: (user: string) => dispatch(projectsActions.fetchProjectsNames(user))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(BuildCreate));
