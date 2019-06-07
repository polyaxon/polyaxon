import * as _ from 'lodash';
import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../actions/projects';
import ProjectOverview from '../../components/projects/projectOverview';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { getProjectUniqueName } from '../../constants/utils';
import { ProjectModel } from '../../models/project';
import { getErrorsByIds } from '../../utils/errors';
import { getIsLoading } from '../../utils/isLoading';

interface Props extends RouteComponentProps<any> {
  project: ProjectModel;
}

export function mapStateToProps(state: AppState, props: Props) {
  const projectUniqueName = getProjectUniqueName(
    props.match.params.user,
    props.match.params.projectName);

  const isGetLoading = getIsLoading(state.loadingIndicators.projects.byIds, projectUniqueName, ACTIONS.GET);
  const isUpdateLoading = getIsLoading(state.loadingIndicators.projects.byIds, projectUniqueName, ACTIONS.UPDATE);
  const isSetGitLoading = getIsLoading(state.loadingIndicators.projects.byIds, projectUniqueName, ACTIONS.SET_GIT);
  const UpdateErrors = getErrorsByIds(state.alerts.projects.byIds, isUpdateLoading, projectUniqueName, ACTIONS.UPDATE);
  const setGitErrors = getErrorsByIds(state.alerts.projects.byIds, isUpdateLoading, projectUniqueName, ACTIONS.SET_GIT);
  const propsResults = {
    isGetLoading,
    isUpdateLoading,
    isSetGitLoading,
    UpdateErrors,
    setGitErrors,
  };
  return _.includes(state.projects.uniqueNames, projectUniqueName) ?
    {...propsResults, project: state.projects.byUniqueNames[projectUniqueName]} :
    {...propsResults, project: null};
}

export interface DispatchProps {
  onUpdate: (updateDict: { [key: string]: any }) => actions.ProjectAction;
  onSetGit: (updateDict: { [key: string]: any }) => actions.ProjectAction;
  onFetch: () => actions.ProjectAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ProjectAction>, props: Props): DispatchProps {
  return {
    onUpdate: (updateDict: { [key: string]: any }) => dispatch(
      actions.updateProject(
        getProjectUniqueName(
          props.match.params.user,
          props.match.params.projectName),
        updateDict)),
    onSetGit: (updateDict: { [key: string]: any }) => dispatch(
      actions.setProjectGit(
        getProjectUniqueName(
          props.match.params.user,
          props.match.params.projectName),
        updateDict)),
    onFetch: () => dispatch(
      actions.fetchProject(
        props.match.params.user,
        props.match.params.projectName)),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ProjectOverview));
