import * as React from 'react';

import * as actions from '../actions/group';
import { DEFAULT_FILTER_OPTIONS, FILTER_EXAMPLES } from '../constants/filtering';
import { DEFAULT_SORT_OPTIONS } from '../constants/sorting';
import { FilterOption } from '../interfaces/filterOptions';
import { GroupModel } from '../models/group';
import { EmptyBookmarks } from './empty/emptyBookmarks';
import { EmptyList } from './empty/emptyList';
import { DEFAULT_FILTERS } from './filters/constants';
import Group from './group';
import GroupHeader from './groupHeader';
import PaginatedTable from './paginatedTable';

export interface Props {
  isCurrentUser: boolean;
  groups: GroupModel[];
  count: number;
  useFilters: boolean;
  bookmarks: boolean;
  onCreate: (group: GroupModel) => actions.GroupAction;
  onUpdate: (group: GroupModel) => actions.GroupAction;
  onDelete: (GroupName: string) => actions.GroupAction;
  onStop: (GroupName: string) => actions.GroupAction;
  fetchData: (offset?: number, query?: string, sort?: string) => actions.GroupAction;
}

export default class Groups extends React.Component<Props, {}> {
  public render() {
    const filterOptions = [
      ...DEFAULT_FILTER_OPTIONS,
      {
        filter: 'search_algorithm',
        type: 'value',
        desc: 'search_algorithm: bo or search_algorithm: random|hyperband'
      },
      {
        filter: 'concurrency',
        type: 'scalar',
        desc: FILTER_EXAMPLES.scalar('concurrency'),
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
          {groups.map(
            (group: GroupModel) =>
              <Group
                key={group.unique_name}
                group={group}
                onDelete={() => this.props.onDelete(group.unique_name)}
                onStop={() => this.props.onStop(group.unique_name)}
              />)}
          </tbody>
        </table>
      );
    };

    const empty = this.props.bookmarks ?
      EmptyBookmarks(
        this.props.isCurrentUser,
        'experiment group',
        'group')
      : EmptyList(
        this.props.isCurrentUser,
        'experiment group',
        'group',
        'polyaxon run --help');

    return (
      <PaginatedTable
        count={this.props.count}
        componentEmpty={empty}
        componentList={listGroups()}
        filters={filters}
        fetchData={this.props.fetchData}
        sortOptions={DEFAULT_SORT_OPTIONS}
        filterOptions={filterOptions}
      />
    );
  }
}
