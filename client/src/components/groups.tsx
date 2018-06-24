import * as React from 'react';
import * as _ from 'lodash';

import Group from './group';
import { GroupModel } from '../models/group';
import { DEFAULT_FILTERS } from './filters/constants';
import PaginatedList from './paginatedList';
import { EmptyList } from './emptyList';
import GroupHeader from './groupHeader';
import * as actions from '../actions/group';

export interface Props {
  isCurrentUser: boolean;
  groups: GroupModel[];
  count: number;
  onCreate: (group: GroupModel) => actions.GroupAction;
  onUpdate: (group: GroupModel) => actions.GroupAction;
  onDelete: (group: GroupModel) => actions.GroupAction;
  fetchData: (offset?: number, query?: string, sort?: string) => actions.GroupAction;
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
        filters={DEFAULT_FILTERS}
        fetchData={this.props.fetchData}
      />
    );
  }
}
