import * as React from 'react';
import * as _ from 'lodash';

import Group from './group';
import { GroupModel } from '../models/group';
import PaginatedList from '../components/paginatedList';

export interface Props {
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
      if (groups.length === 0) {
        return (
          <div className="row">
            <div className="col-md-offset-2 col-md-8">
              <div className="jumbotron jumbotron-action text-center">
                <h3>You don't have any experiment group</h3>
                <img src="/static/images/group.svg" alt="group" className="empty-icon"/>
                <div>
                  You can start new experiment group by using CLI: <b>polyaxon run --help</b>
                </div>
              </div>
            </div>
          </div>
        );
      }
      return (
        <div className="col-md-12">
          <ul>
            {groups.filter(
              (group: GroupModel) => _.isNil(group.deleted) || !group.deleted
            ).map(
              (group: GroupModel) =>
                <li className="list-item" key={group.unique_name}>
                  <Group group={group} onDelete={() => this.props.onDelete(group)}/>
                </li>)}
          </ul>
        </div>
      );
    };
    return (
      <PaginatedList
        count={this.props.count}
        componentList={listGroups()}
        fetchData={this.props.fetchData}
      />
    );
  }
}
