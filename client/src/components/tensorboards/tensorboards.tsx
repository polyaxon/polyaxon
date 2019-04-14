import * as React from 'react';

import * as search_actions from '../../actions/search';
import * as actions from '../../actions/tensorboards';
import { JOB_FILTER_OPTIONS } from '../../constants/filtering';
import { DEFAULT_SORT_OPTIONS } from '../../constants/sorting';
import { SearchModel } from '../../models/search';
import { TensorboardModel } from '../../models/tensorboard';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';
import { isLive } from '../../utils/isLive';
import { EmptyArchives } from '../empty/emptyArchives';
import { EmptyBookmarks } from '../empty/emptyBookmarks';
import { EmptyList } from '../empty/emptyList';
import { DEFAULT_FILTERS } from '../filters/constants';
import PaginatedTable from '../tables/paginatedTable';
import Tensorboard from './tensorboard';
import TensorboardHeader from './tensorboardHeader';

export interface Props {
  isCurrentUser: boolean;
  tensorboards: TensorboardModel[];
  count: number;
  useFilters: boolean;
  showBookmarks: boolean;
  showDeleted: boolean;
  endpointList: string;
  onUpdate: (tensorboard: TensorboardModel) => actions.TensorboardAction;
  onDelete: (tensorboardName: string) => actions.TensorboardAction;
  onStop: (tensorboardName: string) => actions.TensorboardAction;
  onArchive: (tensorboardName: string) => actions.TensorboardAction;
  onRestore: (tensorboardName: string) => actions.TensorboardAction;
  bookmark: (tensorboardName: string) => actions.TensorboardAction;
  unbookmark: (tensorboardName: string) => actions.TensorboardAction;
  fetchData: (offset?: number, query?: string, sort?: string) => actions.TensorboardAction;
  fetchSearches?: () => search_actions.SearchAction;
  createSearch?: (data: SearchModel) => search_actions.SearchAction;
  deleteSearch?: (searchId: number) => search_actions.SearchAction;
  isLoading: boolean;
  errors: any;
}

export default class Tensorboards extends React.Component<Props, {}> {
  public render() {
    const filters = this.props.useFilters ? DEFAULT_FILTERS : false;
    const tensorboards = this.props.tensorboards;
    const listTensorboards = () => {
      return (
        <table className="table table-hover table-responsive">
          <tbody>
          {TensorboardHeader()}
          {tensorboards
            .filter(
              (tensorboard: TensorboardModel) =>
                (!this.props.showDeleted && isLive(tensorboard)) || (this.props.showDeleted && !isLive(tensorboard)))
            .map(
            (tensorboard: TensorboardModel) =>
              <Tensorboard
                key={tensorboard.unique_name}
                tensorboard={tensorboard}
                onDelete={() => this.props.onDelete(tensorboard.unique_name)}
                onStop={() => this.props.onStop(tensorboard.unique_name)}
                onArchive={() => this.props.onArchive(tensorboard.unique_name)}
                onRestore={() => this.props.onRestore(tensorboard.unique_name)}
                showBookmarks={this.props.showBookmarks}
                bookmark={() => this.props.bookmark(tensorboard.unique_name)}
                unbookmark={() => this.props.unbookmark(tensorboard.unique_name)}
              />)}
          </tbody>
        </table>
      );
    };

    let empty: any;
    if (this.props.endpointList === BOOKMARKS) {
      empty = EmptyBookmarks(
        this.props.isCurrentUser,
        'tensorboard',
        'dashboard');
    } else if (this.props.endpointList === ARCHIVES) {
       empty = EmptyArchives(
        this.props.isCurrentUser,
        'tensorboard',
        'dashboard');
    } else {
      empty = EmptyList(
        this.props.isCurrentUser,
        'tensorboard',
        'dashboard',
        'polyaxon tensorboard --help');
    }

    return (
      <PaginatedTable
        isLoading={this.props.isLoading}
        errors={this.props.errors}
        count={this.props.count}
        componentList={listTensorboards()}
        componentEmpty={empty}
        filters={filters}
        fetchData={this.props.fetchData}
        fetchSearches={this.props.fetchSearches}
        createSearch={this.props.createSearch}
        deleteSearch={this.props.deleteSearch}
        sortOptions={DEFAULT_SORT_OPTIONS}
        filterOptions={JOB_FILTER_OPTIONS}
      />
    );
  }
}
