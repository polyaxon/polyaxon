import * as _ from 'lodash';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../actions/project';
import ProjectDetail from '../components/projectDetail';
import { AppState } from '../constants/types';
import { getProjectUniqueName } from '../constants/utils';

export function mapStateToProps(state: AppState, params: any) {
  const projectUniqueName = getProjectUniqueName(
    params.match.params.user,
    params.match.params.projectName);
  return _.includes(state.projects.uniqueNames, projectUniqueName) ?
    {project: state.projects.byUniqueNames[projectUniqueName]} :
    {project: null};
}

export interface DispatchProps {
  onDelete: () => actions.ProjectAction;
  fetchData?: () => actions.ProjectAction;
  bookmark: () => actions.ProjectAction;
  unbookmark: () => actions.ProjectAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ProjectAction>, params: any): DispatchProps {
  return {
    onDelete: () => dispatch(
      actions.deleteProject(
        getProjectUniqueName(
          params.match.params.user,
          params.match.params.projectName),
        true)),
    fetchData: () => dispatch(
      actions.fetchProject(
        params.match.params.user,
        params.match.params.projectName)),
    bookmark: () => dispatch(
      actions.bookmark(
        params.match.params.user,
        params.match.params.projectName)),
    unbookmark: () => dispatch(
      actions.unbookmark(
        params.match.params.user,
        params.match.params.projectName)),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ProjectDetail));
