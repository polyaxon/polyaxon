import * as React from 'react';

import * as actions from '../../actions/groups';
import * as search_actions from '../../actions/search';
import { GroupModel } from '../../models/group';
import { SearchModel } from '../../models/search';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';
import { isLive } from '../../utils/isLive';
import { EmptyArchives } from '../empty/emptyArchives';
import { EmptyBookmarks } from '../empty/emptyBookmarks';
import { EmptyList } from '../empty/emptyList';
import { DEFAULT_FILTERS } from '../filters/constants';
import { getColumnFilters, getGroupColumnOptions} from '../tables/columns';
import PaginatedTable from '../tables/paginatedTable';
import { BASE_SORT_OPTIONS } from '../tables/sorters';
import Group from './group';
import GroupHeader from './groupHeader';

export interface Props {
  isCurrentUser: boolean;
  groups: GroupModel[];
  count: number;
  useFilters: boolean;
  showBookmarks: boolean;
  showDeleted: boolean;
  endpointList: string;
  onCreate: (group: GroupModel) => actions.GroupAction;
  onUpdate: (group: GroupModel) => actions.GroupAction;
  onDelete: (GroupName: string) => actions.GroupAction;
  onStop: (GroupName: string) => actions.GroupAction;
  onArchive: (GroupName: string) => actions.GroupAction;
  onRestore: (GroupName: string) => actions.GroupAction;
  bookmark: (GroupName: string) => actions.GroupAction;
  unbookmark: (GroupName: string) => actions.GroupAction;
  fetchData: (offset?: number, query?: string, sort?: string) => actions.GroupAction;
  fetchSearches?: () => search_actions.SearchAction;
  createSearch?: (data: SearchModel) => search_actions.SearchAction;
  deleteSearch?: (searchId: number) => search_actions.SearchAction;
  isLoading: boolean;
  errors: any;
}

export default class Groups extends React.Component<Props, {}> {
  public render() {
    const filters = this.props.useFilters ? DEFAULT_FILTERS : false;
    const groups = this.props.groups;
    const listGroups = () => {
      return (
        <table className="table table-hover table-responsive">
          <tbody>
          {GroupHeader()}
          {groups
            .filter((group: GroupModel) =>
              (!this.props.showDeleted && isLive(group)) || (this.props.showDeleted && !isLive(group)))
            .map(
            (group: GroupModel) =>
              <Group
                key={group.unique_name}
                group={group}
                onDelete={() => this.props.onDelete(group.unique_name)}
                onStop={() => this.props.onStop(group.unique_name)}
                onArchive={() => this.props.onArchive(group.unique_name)}
                onRestore={() => this.props.onRestore((group.unique_name))}
                showBookmarks={this.props.showBookmarks}
                bookmark={() => this.props.bookmark(group.unique_name)}
                unbookmark={() => this.props.unbookmark(group.unique_name)}
              />)}
          </tbody>
        </table>
      );
    };

    let empty: any;
    if (this.props.endpointList === BOOKMARKS) {
      empty = EmptyBookmarks(
        this.props.isCurrentUser,
        'experiment group',
        'group');
    } else if (this.props.endpointList === ARCHIVES) {
       empty = EmptyArchives(
        this.props.isCurrentUser,
        'experiment group',
        'group');
    } else {
      empty = EmptyList(
        this.props.isCurrentUser,
        'experiment group',
        'group',
        'polyaxon run --help');
    }

    return (
      <PaginatedTable
        isLoading={this.props.isLoading}
        errors={this.props.errors}
        count={this.props.count}
        componentEmpty={empty}
        componentList={listGroups()}
        filters={filters}
        fetchData={this.props.fetchData}
        fetchSearches={this.props.fetchSearches}
        createSearch={this.props.createSearch}
        deleteSearch={this.props.deleteSearch}
        sortOptions={BASE_SORT_OPTIONS}
        columnOptions={getColumnFilters(getGroupColumnOptions())}
      />
    );
  }
}
