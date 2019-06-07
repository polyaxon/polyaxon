import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import Notebooks from '../../components/notebooks/notebooks';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { NotebookModel } from '../../models/notebook';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';

import * as actions from '../../actions/notebooks';
import * as search_actions from '../../actions/search';
import { ACTIONS } from '../../constants/actions';
import { SearchModel } from '../../models/search';
import { getErrorsGlobal } from '../../utils/errors';
import { getLastFetchedNotebooks } from '../../utils/states';

interface Props extends RouteComponentProps<any> {
  user?: string;
  projectName?: string;
  endpointList?: string;
  useFilters?: boolean;
  showBookmarks?: boolean;
  showDeleted?: boolean;
  fetchData?: () => any;
}

export function mapStateToProps(state: AppState, props: Props) {
  const cUser = props.user || props.match.params.user;
  const results = getLastFetchedNotebooks(state.notebooks);
  const isLoading = isTrue(state.loadingIndicators.notebooks.global.fetch);
  return {
    isCurrentUser: state.auth.user === cUser,
    notebooks: results.notebooks,
    count: results.count,
    useFilters: isTrue(props.useFilters),
    showBookmarks: isTrue(props.showBookmarks),
    showDeleted: isTrue(props.showDeleted),
    endpointList: props.endpointList,
    isLoading,
    errors: getErrorsGlobal(state.alerts.notebooks.global, isLoading, ACTIONS.FETCH),
  };
}

export interface DispatchProps {
  onDelete: (notebookName: string) => actions.NotebookAction;
  onStop: (notebookName: string) => actions.NotebookAction;
  onArchive: (notebookName: string) => actions.NotebookAction;
  onRestore: (notebookName: string) => actions.NotebookAction;
  onUpdate?: (notebook: NotebookModel) => actions.NotebookAction;
  bookmark?: (notebookName: string) => actions.NotebookAction;
  unbookmark?: (notebookName: string) => actions.NotebookAction;
  fetchData?: (offset?: number, query?: string, sort?: string) => actions.NotebookAction;
  fetchSearches?: () => search_actions.SearchAction;
  createSearch?: (data: SearchModel) => search_actions.SearchAction;
  deleteSearch?: (searchId: number) => search_actions.SearchAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.NotebookAction>, props: Props): DispatchProps {
  const cUser = props.user || props.match.params.user;
  const cProjectName = props.projectName || `${cUser}.${props.match.params.projectName}`;

  return {
    onDelete: (notebookName: string) => dispatch(actions.deleteNotebook(notebookName)),
    onStop: (notebookName: string) => dispatch(actions.stopNotebook(notebookName)),
    onArchive: (notebookName: string) => dispatch(actions.archiveNotebook(notebookName)),
    onRestore: (notebookName: string) => dispatch(actions.restoreNotebook(notebookName)),
    bookmark: (notebookName: string) => dispatch(actions.bookmark(notebookName)),
    unbookmark: (notebookName: string) => dispatch(actions.unbookmark(notebookName)),
    onUpdate: (notebook: NotebookModel) => dispatch(actions.updateNotebookSuccessActionCreator(notebook)),
    fetchSearches: () => {
      if (cProjectName) {
        return dispatch(search_actions.fetchNotebookSearches(cProjectName));
      } else {
        throw new Error('Notebooks container does not have project.');
      }
    },
    createSearch: (data: SearchModel) => {
      if (cProjectName) {
        return dispatch(search_actions.createNotebookSearch(cProjectName, data));
      } else {
        throw new Error('Notebooks container does not have project.');
      }
    },
    deleteSearch: (searchId: number) => {
      if (cProjectName) {
        return dispatch(search_actions.deleteNotebookSearch(cProjectName, searchId));
      } else {
        throw new Error('Notebooks container does not have project.');
      }
    },
    fetchData: (offset?: number, query?: string, sort?: string) => {
      const filters: { [key: string]: number | boolean | string } = {};
      if (query) {
        filters.query = query;
      }
      if (sort) {
        filters.sort = sort;
      }
      if (offset) {
        filters.offset = offset;
      }
      if (props.endpointList === BOOKMARKS) {
        return dispatch(actions.fetchBookmarkedNotebooks(cUser, filters));
      } else if (props.endpointList === ARCHIVES) {
        return dispatch(actions.fetchArchivedNotebooks(cUser, filters));
      } else if (cProjectName) {
        return dispatch(actions.fetchNotebooks(cProjectName, filters));
      } else {
        throw new Error('Notebooks container expects either a project name or bookmarks or archives.');
      }
    }
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Notebooks));
