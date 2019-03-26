import * as _ from 'lodash';
import { connect } from 'react-redux';
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

interface OwnProps {
  user: string;
  projectName?: string;
  endpointList?: string;
  useFilters?: boolean;
  showBookmarks?: boolean;
  showDeleted?: boolean;
  fetchData?: () => any;
}

export function mapStateToProps(state: AppState, ownProps: OwnProps) {
  const useLastFetched = () => {
    const notebookNames = state.notebooks.lastFetched.names;
    const count = state.notebooks.lastFetched.count;
    const notebooks: NotebookModel[] = [];
    notebookNames.forEach(
      (build: string, idx: number) => {
        notebooks.push(state.notebooks.byUniqueNames[build]);
      });
    return {notebooks, count};
  };
  const results = useLastFetched();

  const isLoading = isTrue(state.loadingIndicators.notebooks.global.fetch);
  return {
    isCurrentUser: state.auth.user === ownProps.user,
    notebooks: results.notebooks,
    count: results.count,
    useFilters: isTrue(ownProps.useFilters),
    showBookmarks: isTrue(ownProps.showBookmarks),
    showDeleted: isTrue(ownProps.showDeleted),
    endpointList: ownProps.endpointList,
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

export function mapDispatchToProps(dispatch: Dispatch<actions.NotebookAction>, ownProps: OwnProps): DispatchProps {
  return {
    onDelete: (notebookName: string) => dispatch(actions.deleteNotebook(notebookName)),
    onStop: (notebookName: string) => dispatch(actions.stopNotebook(notebookName)),
    onArchive: (notebookName: string) => dispatch(actions.archiveNotebook(notebookName)),
    onRestore: (notebookName: string) => dispatch(actions.restoreNotebook(notebookName)),
    bookmark: (notebookName: string) => dispatch(actions.bookmark(notebookName)),
    unbookmark: (notebookName: string) => dispatch(actions.unbookmark(notebookName)),
    onUpdate: (notebook: NotebookModel) => dispatch(actions.updateNotebookSuccessActionCreator(notebook)),
    fetchSearches: () => {
      if (ownProps.projectName) {
        return dispatch(search_actions.fetchNotebookSearches(ownProps.projectName));
      } else {
        throw new Error('Notebooks container does not have project.');
      }
    },
    createSearch: (data: SearchModel) => {
      if (ownProps.projectName) {
        return dispatch(search_actions.createNotebookSearch(ownProps.projectName, data));
      } else {
        throw new Error('Notebooks container does not have project.');
      }
    },
    deleteSearch: (searchId: number) => {
      if (ownProps.projectName) {
        return dispatch(search_actions.deleteNotebookSearch(ownProps.projectName, searchId));
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
      if (_.isNil(ownProps.projectName) && ownProps.endpointList === BOOKMARKS) {
        return dispatch(actions.fetchBookmarkedNotebooks(ownProps.user, filters));
      } else if (_.isNil(ownProps.projectName) && ownProps.endpointList === ARCHIVES) {
        return dispatch(actions.fetchArchivedNotebooks(ownProps.user, filters));
      } else if (ownProps.projectName) {
        return dispatch(actions.fetchNotebooks(ownProps.projectName, filters));
      } else {
        throw new Error('Notebooks container expects either a project name or bookmarks or archives.');
      }
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Notebooks);
