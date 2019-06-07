import { connect } from 'react-redux';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import { Dispatch } from 'redux';

import Tensorboards from '../../components/tensorboards/tensorboards';
import { AppState } from '../../constants/types';
import { isTrue } from '../../constants/utils';
import { TensorboardModel } from '../../models/tensorboard';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';

import * as search_actions from '../../actions/search';
import * as actions from '../../actions/tensorboards';
import { ACTIONS } from '../../constants/actions';
import { SearchModel } from '../../models/search';
import { getErrorsGlobal } from '../../utils/errors';
import { getLastFetchedTensorboards } from '../../utils/states';

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
  const results = getLastFetchedTensorboards(state.tensorboards);
  const isLoading = isTrue(state.loadingIndicators.tensorboards.global.fetch);
  return {
    isCurrentUser: state.auth.user === cUser,
    tensorboards: results.tensorboards,
    count: results.count,
    useFilters: isTrue(props.useFilters),
    showBookmarks: isTrue(props.showBookmarks),
    showDeleted: isTrue(props.showDeleted),
    endpointList: props.endpointList,
    isLoading,
    errors: getErrorsGlobal(state.alerts.tensorboards.global, isLoading, ACTIONS.FETCH),
  };
}

export interface DispatchProps {
  onCreate?: (tensorboard: TensorboardModel) => actions.TensorboardAction;
  onDelete: (tensorboardName: string) => actions.TensorboardAction;
  onStop: (tensorboardName: string) => actions.TensorboardAction;
  onArchive: (tensorboardName: string) => actions.TensorboardAction;
  onRestore: (tensorboardName: string) => actions.TensorboardAction;
  onUpdate?: (tensorboard: TensorboardModel) => actions.TensorboardAction;
  bookmark?: (tensorboardName: string) => actions.TensorboardAction;
  unbookmark?: (tensorboardName: string) => actions.TensorboardAction;
  fetchData?: (offset?: number, query?: string, sort?: string) => actions.TensorboardAction;
  fetchSearches?: () => search_actions.SearchAction;
  createSearch?: (data: SearchModel) => search_actions.SearchAction;
  deleteSearch?: (searchId: number) => search_actions.SearchAction;
}

export function mapDispatchToProps(dispatch: Dispatch<actions.TensorboardAction>, props: Props): DispatchProps {
  const cUser = props.user || props.match.params.user;
  const cProjectName = props.projectName || `${cUser}.${props.match.params.projectName}`;

  return {
    onDelete: (tensorboardName: string) => dispatch(actions.deleteTensorboard(tensorboardName)),
    onStop: (tensorboardName: string) => dispatch(actions.stopTensorboard(tensorboardName)),
    onArchive: (tensorboardName: string) => dispatch(actions.archiveTensorboard(tensorboardName)),
    onRestore: (tensorboardName: string) => dispatch(actions.restoreTensorboard(tensorboardName)),
    bookmark: (tensorboardName: string) => dispatch(actions.bookmark(tensorboardName)),
    unbookmark: (tensorboardName: string) => dispatch(actions.unbookmark(tensorboardName)),
    onUpdate: (tensorboard: TensorboardModel) => dispatch(actions.updateTensorboardSuccessActionCreator(tensorboard)),
    fetchSearches: () => {
      if (cProjectName) {
        return dispatch(search_actions.fetchTensorboardSearches(cProjectName));
      } else {
        throw new Error('Tensorboards container does not have project.');
      }
    },
    createSearch: (data: SearchModel) => {
      if (cProjectName) {
        return dispatch(search_actions.createTensorboardSearch(cProjectName, data));
      } else {
        throw new Error('Tensorboards container does not have project.');
      }
    },
    deleteSearch: (searchId: number) => {
      if (cProjectName) {
        return dispatch(search_actions.deleteTensorboardSearch(cProjectName, searchId));
      } else {
        throw new Error('Tensorboards container does not have project.');
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
        return dispatch(actions.fetchBookmarkedTensorboards(cUser, filters));
      } else if (props.endpointList === ARCHIVES) {
        return dispatch(actions.fetchArchivedTensorboards(cUser, filters));
      } else if (cProjectName) {
        return dispatch(actions.fetchTensorboards(cProjectName, filters));
      } else {
        throw new Error('Tensorboards container expects either a project name or bookmarks or archives.');
      }
    }
  };
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Tensorboards));
