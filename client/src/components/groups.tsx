import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../actions/group';
import { GroupModel } from '../models/group';
import { EmptyBookmarks } from './empty/emptyBookmarks';
import { EmptyList } from './empty/emptyList';
import { DEFAULT_FILTERS } from './filters/constants';
import Group from './group';
import GroupHeader from './groupHeader';
import PaginatedList from './paginatedList';

export interface Props {
  isCurrentUser: boolean;
  groups: GroupModel[];
  count: number;
  useFilters: boolean;
  bookmarks: boolean;
  onCreate: (group: GroupModel) => actions.GroupAction;
  onUpdate: (group: GroupModel) => actions.GroupAction;
  onDelete: (group: GroupModel) => actions.GroupAction;
  fetchData: (offset?: number, query?: string, sort?: string) => actions.GroupAction;
}

export default class Groups extends React.Component<Props, Object> {
  public render() {
    const filters = this.props.useFilters ? DEFAULT_FILTERS : false;
    const groups = this.props.groups;
    const listGroups = () => {
      return (
        <ul>
          {groups.filter(
            (group: GroupModel) => _.isNil(group.deleted) || !group.deleted
          ).map(
            (group: GroupModel) =>
              <li className="list-item" key={group.unique_name}>
                <Group group={group} onDelete={() => this.props.onDelete(group)}/>
              </li>)}
        </ul>
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
      <PaginatedList
        count={this.props.count}
        componentEmpty={empty}
        componentHeader={GroupHeader()}
        componentList={listGroups()}
        filters={filters}
        fetchData={this.props.fetchData}
      />
    );
  }
}
