import * as _ from 'lodash';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
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

export function mapStateToProps(state: AppState, params: any) {
  const isLoading = isTrue(state.loadingIndicators.builds.global.create);
  const isProjectEntity = _.isNil(params.match.params.user);
  const projects = isProjectEntity ? getLastFetchedProjects(state.projects).projects : [];
  return {
    user: params.match.params.user || state.auth.user,
    projectName: params.match.params.projectName,
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
  dispatch: Dispatch<buildsActions.BuildAction>, params: any): DispatchProps {
  return {
    onCreate: (build: BuildModel, user?: string, projectName?: string) => dispatch(
      buildsActions.createBuild(
        user || params.match.params.user,
        projectName || params.match.params.projectName,
        build,
        true)),
    fetchProjects: (user: string) => dispatch(projectsActions.fetchProjectsNames(user))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(BuildCreate));
