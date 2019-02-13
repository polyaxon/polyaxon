import * as React from 'react';

import * as actions from '../../actions/build';
import * as search_actions from '../../actions/search';
import { BUILD_FILTER_OPTIONS } from '../../constants/filtering';
import { DEFAULT_SORT_OPTIONS } from '../../constants/sorting';
import { BuildModel } from '../../models/build';
import { SearchModel } from '../../models/search';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';
import { isLive } from '../../utils/isLive';
import { EmptyArchives } from '../empty/emptyArchives';
import { EmptyBookmarks } from '../empty/emptyBookmarks';
import { EmptyList } from '../empty/emptyList';
import { DEFAULT_FILTERS } from '../filters/constants';
import PaginatedTable from '../tables/paginatedTable';
import Build from './build';
import BuildHeader from './buildHeader';

export interface Props {
  isCurrentUser: boolean;
  builds: BuildModel[];
  count: number;
  useFilters: boolean;
  showBookmarks: boolean;
  showDeleted: boolean;
  endpointList: string;
  onCreate: (build: BuildModel) => actions.BuildAction;
  onUpdate: (build: BuildModel) => actions.BuildAction;
  onDelete: (buildName: string) => actions.BuildAction;
  onStop: (buildName: string) => actions.BuildAction;
  onArchive: (buildName: string) => actions.BuildAction;
  onRestore: (buildName: string) => actions.BuildAction;
  bookmark: (buildName: string) => actions.BuildAction;
  unbookmark: (buildName: string) => actions.BuildAction;
  fetchData: (offset?: number, query?: string, sort?: string) => actions.BuildAction;
  fetchSearches?: () => search_actions.SearchAction;
  createSearch?: (data: SearchModel) => search_actions.SearchAction;
  deleteSearch?: (searchId: number) => search_actions.SearchAction;
}

export default class Builds extends React.Component<Props, {}> {
  public render() {
    const filters = this.props.useFilters ? DEFAULT_FILTERS : false;
    const builds = this.props.builds;
    const listBuilds = () => {
      return (
        <table className="table table-hover table-responsive">
          <tbody>
          {BuildHeader()}
          {builds
            .filter(
              (build: BuildModel) =>
                (!this.props.showDeleted && isLive(build)) || (this.props.showDeleted && !isLive(build)))
            .map(
            (build: BuildModel) =>
              <Build
                key={build.unique_name}
                build={build}
                onDelete={() => this.props.onDelete(build.unique_name)}
                onStop={() => this.props.onStop(build.unique_name)}
                onArchive={() => this.props.onArchive(build.unique_name)}
                onRestore={() => this.props.onRestore(build.unique_name)}
                showBookmarks={this.props.showBookmarks}
                bookmark={() => this.props.bookmark(build.unique_name)}
                unbookmark={() => this.props.unbookmark(build.unique_name)}
              />)}
          </tbody>
        </table>
      );
    };

    let empty: any;
    if (this.props.endpointList === BOOKMARKS) {
      empty = EmptyBookmarks(
        this.props.isCurrentUser,
        'build',
        'build');
    } else if (this.props.endpointList === ARCHIVES) {
       empty = EmptyArchives(
        this.props.isCurrentUser,
        'build',
        'build');
    } else {
      empty = EmptyList(
        this.props.isCurrentUser,
        'build',
        'build',
        'polyaxon run --help');
    }

    return (
      <PaginatedTable
        count={this.props.count}
        componentList={listBuilds()}
        componentEmpty={empty}
        filters={filters}
        fetchData={this.props.fetchData}
        fetchSearches={this.props.fetchSearches}
        createSearch={this.props.createSearch}
        deleteSearch={this.props.deleteSearch}
        sortOptions={DEFAULT_SORT_OPTIONS}
        filterOptions={BUILD_FILTER_OPTIONS}
      />
    );
  }
}
