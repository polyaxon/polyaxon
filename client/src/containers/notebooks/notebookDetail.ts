import * as _ from 'lodash';
import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import { AppState } from '../../constants/types';

import * as actions from '../../actions/notebooks';
import NotebookDetail from '../../components/notebooks/notebookDetail';
import { getNotebookUniqueName } from '../../urls/utils';

interface Props extends RouteComponentProps<any> {}

export function mapStateToProps(state: AppState, props: Props) {
  const notebookUniqueName = getNotebookUniqueName(
    props.match.params.user,
    props.match.params.projectName,
    props.match.params.notebookId);
  return _.includes(state.notebooks.uniqueNames, notebookUniqueName) ?
    {notebook: state.notebooks.byUniqueNames[notebookUniqueName]} :
    {notebook: null};
}

export interface DispatchProps {
  onUpdate: (updateDict: { [key: string]: any }) => actions.NotebookAction;
  onDelete: () => actions.NotebookAction;
  onStop: () => actions.NotebookAction;
  onArchive: () => actions.NotebookAction;
  onRestore: () => actions.NotebookAction;
  fetchData?: () => actions.NotebookAction;
  bookmark: () => actions.NotebookAction;
  unbookmark: () => actions.NotebookAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.NotebookAction>, props: Props): DispatchProps {
  return {
    fetchData: () => dispatch(
      actions.fetchNotebook(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.notebookId)),
    onUpdate: (updateDict: { [key: string]: any }) => dispatch(
      actions.updateNotebook(
        getNotebookUniqueName(
          props.match.params.user,
          props.match.params.projectName,
          props.match.params.notebookId),
        updateDict)),
    onDelete: () => dispatch(actions.deleteNotebook(
      getNotebookUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.notebookId),
      true)),
    onStop: () => dispatch(actions.stopNotebook(getNotebookUniqueName(
      props.match.params.user,
      props.match.params.projectName,
      props.match.params.notebookId))),
    onArchive: () => dispatch(actions.archiveNotebook(getNotebookUniqueName(
      props.match.params.user,
      props.match.params.projectName,
      props.match.params.notebookId),
      true)),
    onRestore: () => dispatch(actions.restoreNotebook(getNotebookUniqueName(
      props.match.params.user,
      props.match.params.projectName,
      props.match.params.notebookId))),
    bookmark: () => dispatch(
      actions.bookmark(getNotebookUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.notebookId))),
    unbookmark: () => dispatch(
      actions.unbookmark(getNotebookUniqueName(
        props.match.params.user,
        props.match.params.projectName,
        props.match.params.notebookId))),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(NotebookDetail));
