import * as _ from 'lodash';
import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
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

interface Props extends RouteComponentProps<any> {}

export function mapStateToProps(state: AppState, props: Props) {
  const isLoading = isTrue(state.loadingIndicators.tensorboards.global.create);
  const isProjectEntity = _.isNil(props.match.params.user);
  const projects = isProjectEntity ? getLastFetchedProjects(state.projects).projects : [];

  return {
    user: props.match.params.user || state.auth.user,
    projectName: props.match.params.projectName,
    groupId: props.match.params.groupId,
    experimentId: props.match.params.experimentId,
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
  props: Props): DispatchProps {
  let onCreate: any;
  if (props.match.params.experimentId) {
    onCreate = (tensorboard: TensorboardModel,
                user: string,
                projectName: string) => experimentsActions.startTensorboard(
                  user,
                  projectName,
                  props.match.params.experimentId,
                  tensorboard,
                  true);
  } else if (props.match.params.groupId) {
    onCreate = (tensorboard: TensorboardModel,
                user: string,
                projectName: string) => groupsActions.startTensorboard(
                  user,
                  projectName,
                  props.match.params.groupId,
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
      onCreate(tensorboard, user || props.match.params.user, projectName || props.match.params.projectName)),
    fetchProjects: (user: string) => dispatch(projectsActions.fetchProjectsNames(user))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(TensorboardCreate));
