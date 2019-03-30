import * as _ from 'lodash';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as notebooksActions from '../../actions/projects';
import * as projectsActions from '../../actions/projects';
import NotebookCreate from '../../components/notebooks/notebookCreate';
import { ACTIONS } from '../../constants/actions';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { NotebookModel } from '../../models/notebook';
import { getErrorsGlobal } from '../../utils/errors';
import { getLastFetchedProjects } from '../../utils/states';

export function mapStateToProps(state: AppState, params: any) {
  const isLoading = isTrue(state.loadingIndicators.notebooks.global.create);
  const isProjectEntity = _.isNil(params.match.params.user);
  const projects = isProjectEntity ? getLastFetchedProjects(state.projects).projects : [];

  return {
    user: params.match.params.user || state.auth.user,
    projectName: params.match.params.projectName,
    isProjectEntity,
    isLoading,
    projects,
    errors: getErrorsGlobal(state.alerts.notebooks.global, isLoading, ACTIONS.CREATE),
  };
}

export interface DispatchProps {
  onCreate: (notebook: NotebookModel) => notebooksActions.ProjectAction;
  fetchProjects: (user: string) => projectsActions.ProjectAction;
}

export function mapDispatchToProps(
  dispatch: Dispatch<notebooksActions.ProjectAction>, params: any): DispatchProps {
  return {
    onCreate: (notebook: NotebookModel, user?: string, projectName?: string) => dispatch(
      notebooksActions.startNotebook(
        user || params.match.params.user,
        projectName || params.match.params.projectName,
        notebook,
        true)),
    fetchProjects: (user: string) => dispatch(projectsActions.fetchProjectsNames(user))
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(NotebookCreate));
