import * as React from 'react';

import * as actions from '../actions/statuses';
import { StatusModel } from '../models/status';
import PaginatedList from './paginatedList';
import { EmptyList } from './emptyList';
import StatusHeader from './statusHeader';
import StatusItem from './statusItem';

export interface Props {
  statuses: StatusModel[];
  count: number;
  fetchData: () => actions.StatusesAction;
}

export default class Statuses extends React.Component<Props, Object> {
  public render() {
    const statuses = this.props.statuses;
    const listStatuses = () => {
      return (
        <ul>
          {statuses.map(
            (status: StatusModel) =>
              <li className="list-item" key={status.id}>
                <StatusItem status={status}/>
              </li>)}
        </ul>
      );
    };
    return (
      <PaginatedList
        count={this.props.count}
        componentList={listStatuses()}
        componentHeader={StatusHeader()}
        componentEmpty={
          EmptyList(
            false,
            'status',
            'status')}
        filters={false}
        fetchData={this.props.fetchData}
      />
    );
  }
}
