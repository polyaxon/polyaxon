import * as _ from 'lodash';
import { connect } from 'react-redux';
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
    const tensorboardNames = state.tensorboards.lastFetched.names;
    const count = state.tensorboards.lastFetched.count;
    const tensorboards: TensorboardModel[] = [];
    tensorboardNames.forEach(
      (tensorboard: string, idx: number) => {
        tensorboards.push(state.tensorboards.byUniqueNames[tensorboard]);
      });
    return {tensorboards, count};
  };
  const results = useLastFetched();

  const isLoading = isTrue(state.loadingIndicators.tensorboards.global.fetch);
  return {
    isCurrentUser: state.auth.user === ownProps.user,
    tensorboards: results.tensorboards,
    count: results.count,
    useFilters: isTrue(ownProps.useFilters),
    showBookmarks: isTrue(ownProps.showBookmarks),
    showDeleted: isTrue(ownProps.showDeleted),
    endpointList: ownProps.endpointList,
    isLoading,
    errors: getErrorsGlobal(state.errors.tensorboards.global, isLoading, ACTIONS.FETCH),
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

export function mapDispatchToProps(dispatch: Dispatch<actions.TensorboardAction>, ownProps: OwnProps): DispatchProps {
  return {
    onDelete: (tensorboardName: string) => dispatch(actions.deleteTensorboard(tensorboardName)),
    onStop: (tensorboardName: string) => dispatch(actions.stopTensorboard(tensorboardName)),
    onArchive: (tensorboardName: string) => dispatch(actions.archiveTensorboard(tensorboardName)),
    onRestore: (tensorboardName: string) => dispatch(actions.restoreTensorboard(tensorboardName)),
    bookmark: (tensorboardName: string) => dispatch(actions.bookmark(tensorboardName)),
    unbookmark: (tensorboardName: string) => dispatch(actions.unbookmark(tensorboardName)),
    onUpdate: (tensorboard: TensorboardModel) => dispatch(actions.updateTensorboardSuccessActionCreator(tensorboard)),
    fetchSearches: () => {
      if (ownProps.projectName) {
        return dispatch(search_actions.fetchTensorboardSearches(ownProps.projectName));
      } else {
        throw new Error('Tensorboards container does not have project.');
      }
    },
    createSearch: (data: SearchModel) => {
      if (ownProps.projectName) {
        return dispatch(search_actions.createTensorboardSearch(ownProps.projectName, data));
      } else {
        throw new Error('Tensorboards container does not have project.');
      }
    },
    deleteSearch: (searchId: number) => {
      if (ownProps.projectName) {
        return dispatch(search_actions.deleteTensorboardSearch(ownProps.projectName, searchId));
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
      if (_.isNil(ownProps.projectName) && ownProps.endpointList === BOOKMARKS) {
        return dispatch(actions.fetchBookmarkedTensorboards(ownProps.user, filters));
      } else if (_.isNil(ownProps.projectName) && ownProps.endpointList === ARCHIVES) {
        return dispatch(actions.fetchArchivedTensorboards(ownProps.user, filters));
      } else if (ownProps.projectName) {
        return dispatch(actions.fetchTensorboards(ownProps.projectName, filters));
      } else {
        throw new Error('Tensorboards container expects either a project name or bookmarks or archives.');
      }
    }
  };
}

export default connect(mapStateToProps, mapDispatchToProps)(Tensorboards);
