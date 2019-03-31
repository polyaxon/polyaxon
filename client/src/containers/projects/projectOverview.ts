import * as _ from 'lodash';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../actions/projects';
import ProjectOverview from '../../components/projects/projectOverview';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { getProjectUniqueName } from '../../constants/utils';
import { getErrorsByIds } from '../../utils/errors';
import { getIsLoading } from '../../utils/isLoading';

export function mapStateToProps(state: AppState, params: any) {
  const projectUniqueName = getProjectUniqueName(
    params.match.params.user,
    params.match.params.projectName);

  const isGetLoading = getIsLoading(state.loadingIndicators.projects.byIds, projectUniqueName, ACTIONS.GET);
  const isUpdateLoading = getIsLoading(state.loadingIndicators.projects.byIds, projectUniqueName, ACTIONS.UPDATE);
  const isSetGitLoading = getIsLoading(state.loadingIndicators.projects.byIds, projectUniqueName, ACTIONS.SET_GIT);
  const UpdateErrors = getErrorsByIds(state.alerts.projects.byIds, isUpdateLoading, projectUniqueName, ACTIONS.UPDATE);
  const setGitErrors = getErrorsByIds(state.alerts.projects.byIds, isUpdateLoading, projectUniqueName, ACTIONS.SET_GIT);
  const props = {
    isGetLoading,
    isUpdateLoading,
    isSetGitLoading,
    UpdateErrors,
    setGitErrors,
  };
  return _.includes(state.projects.uniqueNames, projectUniqueName) ?
    {...props, project: state.projects.byUniqueNames[projectUniqueName]} :
    {...props, project: null};
}

export interface DispatchProps {
  onUpdate: (updateDict: { [key: string]: any }) => actions.ProjectAction;
  onSetGit: (updateDict: { [key: string]: any }) => actions.ProjectAction;
  onFetch: () => actions.ProjectAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ProjectAction>, params: any): DispatchProps {
  return {
    onUpdate: (updateDict: { [key: string]: any }) => dispatch(
      actions.updateProject(
        getProjectUniqueName(
          params.match.params.user,
          params.match.params.projectName),
        updateDict)),
    onSetGit: (updateDict: { [key: string]: any }) => dispatch(
      actions.setProjectGit(
        getProjectUniqueName(
          params.match.params.user,
          params.match.params.projectName),
        updateDict)),
    onFetch: () => dispatch(
      actions.fetchProject(
        params.match.params.user,
        params.match.params.projectName)),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ProjectOverview));
