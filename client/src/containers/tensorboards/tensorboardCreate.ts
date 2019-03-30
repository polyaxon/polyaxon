import * as _ from 'lodash';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as experimentsActions from '../../actions/experiments';
import * as groupsActions from '../../actions/groups';
import * as projectsActions from '../../actions/projects';
import TensorboardCreate from '../../components/tensorboards/tensorboardCreate';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { TensorboardModel } from '../../models/tensorboard';
import { getErrorsGlobal } from '../../utils/errors';
import { getLastFetchedProjects } from '../../utils/states';

export function mapStateToProps(state: AppState, params: any) {
  const isLoading = isTrue(state.loadingIndicators.tensorboards.global.create);
  const isProjectEntity = _.isNil(params.match.params.user);
  const projects = isProjectEntity ? getLastFetchedProjects(state.projects).projects : [];

  return {
    user: params.match.params.user || state.auth.user,
    projectName: params.match.params.projectName,
    groupId: params.match.params.groupId,
    experimentId: params.match.params.experimentId,
    isProjectEntity,
    isLoading,
    projects,
    errors: getErrorsGlobal(state.alerts.tensorboards.global, isLoading, ACTIONS.CREATE),
  };
}

export interface DispatchProps {
  onCreate: (tensorboard: TensorboardModel) => experimentsActions.ExperimentAction
    | groupsActions.GroupAction
    | projectsActions.ProjectAction;
  fetchProjects: (user: string) => projectsActions.ProjectAction;
}

export function mapDispatchToProps(
  dispatch: Dispatch<experimentsActions.ExperimentAction | groupsActions.GroupAction | projectsActions.ProjectAction>,
  params: any): DispatchProps {
  let onCreate: any;
  if (params.match.params.experimentId) {
    onCreate = (tensorboard: TensorboardModel,
                user: string,
                projectName: string) => experimentsActions.startTensorboard(
                  user,
                  projectName,
                  params.match.params.experimentId,
                  tensorboard,
                  true);
  } else if (params.match.params.groupId) {
    onCreate = (tensorboard: TensorboardModel,
                user: string,
                projectName: string) => groupsActions.startTensorboard(
                  user,
                  projectName,
                  params.match.params.groupId,
                  tensorboard,
                  true);
  } else {
    onCreate = (tensorboard: TensorboardModel,
                user: string,
                projectName: string) => projectsActions.startTensorboard(
                  user,
                  projectName,
                  tensorboard,
                  true);
  }

  return {
    onCreate: (tensorboard: TensorboardModel, user?: string, projectName?: string) => dispatch(
      onCreate(tensorboard, user || params.match.params.user, projectName || params.match.params.projectName)),
    fetchProjects: (user: string) => dispatch(projectsActions.fetchProjectsNames(user))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(TensorboardCreate));
