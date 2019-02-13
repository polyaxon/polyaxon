import * as React from 'react';

import * as actions from '../../actions/group';
import * as search_actions from '../../actions/search';
import { DEFAULT_FILTER_OPTIONS, FILTER_EXAMPLES } from '../../constants/filtering';
import { DEFAULT_SORT_OPTIONS } from '../../constants/sorting';
import { FilterOption } from '../../interfaces/filterOptions';
import { GroupModel } from '../../models/group';
import { SearchModel } from '../../models/search';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';
import { isLive } from '../../utils/isLive';
import { EmptyArchives } from '../empty/emptyArchives';
import { EmptyBookmarks } from '../empty/emptyBookmarks';
import { EmptyList } from '../empty/emptyList';
import { DEFAULT_FILTERS } from '../filters/constants';
import PaginatedTable from '../tables/paginatedTable';
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
}

export default class Groups extends React.Component<Props, {}> {
  public render() {
    const filterOptions = [
      ...DEFAULT_FILTER_OPTIONS,
      {
        filter: 'search_algorithm',
        type: 'value',
        desc: 'search_algorithm: bo or search_algorithm: random|hyperband',
        icon: 'asterisk'
      },
      {
        filter: 'concurrency',
        type: 'scalar',
        desc: FILTER_EXAMPLES.int('concurrency'),
        icon: 'share-alt'
      }
    ] as FilterOption[];
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
        count={this.props.count}
        componentEmpty={empty}
        componentList={listGroups()}
        filters={filters}
        fetchData={this.props.fetchData}
        fetchSearches={this.props.fetchSearches}
        createSearch={this.props.createSearch}
        deleteSearch={this.props.deleteSearch}
        sortOptions={DEFAULT_SORT_OPTIONS}
        filterOptions={filterOptions}
      />
    );
  }
}
