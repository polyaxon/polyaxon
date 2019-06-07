import * as _ from 'lodash';
import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import * as actions from '../../actions/projects';
import ProjectDetail from '../../components/projects/projectDetail';
import { AppState } from '../../constants/types';
import { getProjectUniqueName } from '../../constants/utils';

interface Props extends RouteComponentProps<any> {}

export function mapStateToProps(state: AppState, props: Props) {
  const projectUniqueName = getProjectUniqueName(
    props.match.params.user,
    props.match.params.projectName);
  return _.includes(state.projects.uniqueNames, projectUniqueName) ?
    {project: state.projects.byUniqueNames[projectUniqueName]} :
    {project: null};
}

export interface DispatchProps {
  onDelete: () => actions.ProjectAction;
  onArchive: () => actions.ProjectAction;
  onRestore: () => actions.ProjectAction;
  stopNotebook: () => actions.ProjectAction;
  stopTensorboard: () => actions.ProjectAction;
  fetchData?: () => actions.ProjectAction;
  bookmark: () => actions.ProjectAction;
  unbookmark: () => actions.ProjectAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.ProjectAction>, props: Props): DispatchProps {
  return {
    onDelete: () => dispatch(
      actions.deleteProject(
        getProjectUniqueName(
          props.match.params.user,
          props.match.params.projectName),
        true)),
    onArchive: () => dispatch(
      actions.archiveProject(
        getProjectUniqueName(
          props.match.params.user,
          props.match.params.projectName),
        true)),
    onRestore: () => dispatch(
      actions.restoreProject(
        getProjectUniqueName(
          props.match.params.user,
          props.match.params.projectName))),
    stopNotebook: () => dispatch(
      actions.stopNotebook(
        getProjectUniqueName(
          props.match.params.user,
          props.match.params.projectName))),
    stopTensorboard: () => dispatch(
      actions.stopTensorboard(
        getProjectUniqueName(
          props.match.params.user,
          props.match.params.projectName))),
    fetchData: () => dispatch(
      actions.fetchProject(
        props.match.params.user,
        props.match.params.projectName)),
    bookmark: () => dispatch(
      actions.bookmark(getProjectUniqueName(
        props.match.params.user,
        props.match.params.projectName))),
    unbookmark: () => dispatch(
      actions.unbookmark(getProjectUniqueName(
        props.match.params.user,
        props.match.params.projectName))),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(ProjectDetail));
