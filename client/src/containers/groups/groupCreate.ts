import * as _ from 'lodash';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as groupsActions from '../../actions/groups';
import * as projectsActions from '../../actions/projects';
import GroupCreate from '../../components/groups/groupCreate';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { GroupModel } from '../../models/group';
import { getErrorsGlobal } from '../../utils/errors';
import { getLastFetchedProjects } from '../../utils/states';

export function mapStateToProps(state: AppState, params: any) {
  const isLoading = isTrue(state.loadingIndicators.groups.global.create);
  const isProjectEntity = _.isNil(params.match.params.user);
  const projects = isProjectEntity ? getLastFetchedProjects(state.projects).projects : [];

  return {
    user: params.match.params.user || state.auth.user,
    projectName: params.match.params.projectName,
    isProjectEntity,
    isLoading,
    projects,
    errors: getErrorsGlobal(state.alerts.groups.global, isLoading, ACTIONS.CREATE),
  };
}

export interface DispatchProps {
  onCreate: (group: GroupModel) => groupsActions.GroupAction;
  fetchProjects: (user: string) => projectsActions.ProjectAction;
}

export function mapDispatchToProps(
  dispatch: Dispatch<groupsActions.GroupAction>, params: any): DispatchProps {
  return {
    onCreate: (group: GroupModel, user?: string, projectName?: string) => dispatch(
      groupsActions.createGroup(
        user || params.match.params.user,
        projectName || params.match.params.projectName,
        group,
        true)),
    fetchProjects: (user: string) => dispatch(projectsActions.fetchProjectsNames(user))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(GroupCreate));
