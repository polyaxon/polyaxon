import * as _ from 'lodash';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import { AppState } from '../../constants/types';

import * as actions from '../../actions/notebook';
import NotebookDetail from '../../components/notebooks/notebookDetail';
import { getNotebookUniqueName } from '../../constants/utils';

export function mapStateToProps(state: AppState, params: any) {
  const notebookUniqueName = getNotebookUniqueName(
    params.match.params.user,
    params.match.params.projectName,
    params.match.params.notebookId);
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

export function mapDispatchToProps(dispatch: Dispatch<actions.NotebookAction>, params: any): DispatchProps {
  return {
    fetchData: () => dispatch(
      actions.fetchNotebook(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.notebookId)),
    onUpdate: (updateDict: { [key: string]: any }) => dispatch(
      actions.updateNotebook(
        getNotebookUniqueName(
          params.match.params.user,
          params.match.params.projectName,
          params.match.params.notebookId),
        updateDict)),
    onDelete: () => dispatch(actions.deleteNotebook(
      getNotebookUniqueName(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.notebookId),
      true)),
    onStop: () => dispatch(actions.stopNotebook(getNotebookUniqueName(
      params.match.params.user,
      params.match.params.projectName,
      params.match.params.notebookId))),
    onArchive: () => dispatch(actions.archiveNotebook(getNotebookUniqueName(
      params.match.params.user,
      params.match.params.projectName,
      params.match.params.notebookId),
      true)),
    onRestore: () => dispatch(actions.restoreNotebook(getNotebookUniqueName(
      params.match.params.user,
      params.match.params.projectName,
      params.match.params.notebookId))),
    bookmark: () => dispatch(
      actions.bookmark(getNotebookUniqueName(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.notebookId))),
    unbookmark: () => dispatch(
      actions.unbookmark(getNotebookUniqueName(
        params.match.params.user,
        params.match.params.projectName,
        params.match.params.notebookId))),
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(NotebookDetail));
