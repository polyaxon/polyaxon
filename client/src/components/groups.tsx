import * as React from 'react';
import * as _ from 'lodash';

import Group from './group';
import { GroupModel } from '../models/group';
import PaginatedList from '../components/paginatedList';
import { EmptyList } from './emptyList';
import GroupHeader from './groupHeader';

export interface Props {
  isCurrentUser: boolean;
  groups: GroupModel[];
  count: number;
  onCreate: (group: GroupModel) => any;
  onUpdate: (group: GroupModel) => any;
  onDelete: (group: GroupModel) => any;
  fetchData: (currentPage: number) => any;
}

export default class Groups extends React.Component<Props, Object> {
  public render() {
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
    return (
      <PaginatedList
        count={this.props.count}
        componentEmpty={EmptyList(
          this.props.isCurrentUser,
          'experiment group',
          'group',
          'polyaxon run --help')}
        componentHeader={GroupHeader()}
        componentList={listGroups()}
        fetchData={this.props.fetchData}
      />
    );
  }
}
